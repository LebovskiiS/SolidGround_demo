import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoProject.settings')

import django
django.setup()

from rest_framework.test import APITestCase
from rest_framework import status
from django.core.management import call_command
from django.db.models.signals import post_save, post_migrate
from django.db import connection
from django.contrib.auth.models import User
from event.models import AlarmScenario
from event.signals import create_alarm_scenarios
from main.models import UserInfo
from main.signals import create_user_info, create_music
from DjangoProject.settings import API_VERSION, PASSWORD_FOR_TESTS, USERNAME_FOR_TESTS
from .logger import logger


def flush_with_constraints():

    with connection.cursor() as cursor:
        if connection.vendor == 'postgresql':
            cursor.execute("SET CONSTRAINTS ALL DEFERRED;")
        elif connection.vendor == 'sqlite':
            print("*** SQLite detected: Skipping 'SET CONSTRAINTS' ***")
        else:
            raise NotImplementedError(f"flush_with_constraints not supported for {connection.vendor}.")







def registration_for_tests(client, registration_url):
    call_command('flush', '--noinput')
    data = {
        'username': USERNAME_FOR_TESTS,
        'password': PASSWORD_FOR_TESTS,
        'email': 'test@example.com'
    }
    response = client.post(registration_url, data, format='json')
    if response.status_code != status.HTTP_201_CREATED:
        print(f"Registration failed. Status code: {response.status_code}, Response: {response.content}")

def login_for_tests(client, login_url):
    data = {
        'username': USERNAME_FOR_TESTS,
        'password': PASSWORD_FOR_TESTS
    }
    response = client.post(login_url, data, format='json')
    if response.status_code != status.HTTP_200_OK:
        print(f"Login failed. Status code: {response.status_code}, Response: {response.content}")
        return None
    return response.data['token']





class TriggerAlarmTestCase(APITestCase):
    def setUp(self):
        super().setUp()

        flush_with_constraints()

        post_save.disconnect(receiver=create_user_info, sender=User)
        post_migrate.disconnect(receiver=create_music, dispatch_uid="create_music_post_migrate")
        post_migrate.disconnect(receiver=create_alarm_scenarios, dispatch_uid="create_alarm_scenarios_post_migrate")
        self.user_id = 1
        self.registration_url = f'/api/{API_VERSION}/user/registration/'
        self.login_url = f'/api/{API_VERSION}/user/login/'
        self.trigger_url = f'/api/{API_VERSION}/event/trigger/{self.user_id}/'

        registration_for_tests(self.client, self.registration_url)
        test_user = User.objects.first()
        UserInfo.objects.create(user=test_user)

        self.token = login_for_tests(self.client, self.login_url)

        self._create_alarm_scenarios()

    def _create_alarm_scenarios(self):
        scenarios = [
            (1, 'Off', False, False, False),  # id, name, play_music, notify_contact, notify_therapist
            (2, 'Pattern 1', True, False, False),
            (3, 'Pattern 2', True, True, True),
            (4, 'Pattern 3', True, False, True),
        ]

        for id, name, play_music, notify_contact, notify_therapist in scenarios:
            AlarmScenario.objects.update_or_create(
                id=id,
                defaults={
                    'name': name,
                    'play_music': play_music,
                    'notify_contact': notify_contact,
                    'notify_therapist': notify_therapist
                }
            )

    def test_trigger(self):
        logger.info('Starting test_trigger')
        logger.info(
            f"Testing URL: {self.trigger_url}"
        )


        test_user = User.objects.first()
        user_info = UserInfo.objects.get(user=test_user)
        scenario = AlarmScenario.objects.get(id=2)  # Pattern 1 with play_music=True
        user_info.scenario = scenario
        user_info.save()

        headers = {
            'Authorization': f'token {self.token}'
        }

        response = self.client.get(self.trigger_url, format='json', HTTP_AUTHORIZATION=headers['Authorization'])

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['scenario'], scenario.name)
