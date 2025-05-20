from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.management import call_command
from event.models import AlarmScenario
from DjangoProject.settings import API_VERSION, PASSWORD_FOR_TESTS, USERNAME_FOR_TESTS
from main.exceptions import RegistrationInTestsError
from django.db import connection
from django.test import override_settings
from django.db.models.signals import post_save, post_migrate
from main.signals import create_user_info, create_music



assert connection.vendor == 'sqlite', "Test database is not using SQLite!"



def flush_with_constraints():

    with connection.cursor() as cursor:
        if connection.vendor == 'postgresql':
            cursor.execute("SET CONSTRAINTS ALL DEFERRED;")
        elif connection.vendor == 'sqlite':
            print("*** SQLite detected: Skipping 'SET CONSTRAINTS' ***")
        else:
            raise NotImplementedError(f"flush_with_constraints not supported for {connection.vendor}.")


def registration_for_tests(client, registration_url):
    try:
        flush_with_constraints()
        data = {
            'username': USERNAME_FOR_TESTS,
            'password': PASSWORD_FOR_TESTS
        }
        response = client.post(registration_url, data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            raise RegistrationInTestsError("User registration failed.")
    except Exception as e:
        print(f"Registration failed: {e}")
        raise RegistrationInTestsError(str(e))


class RegistrationTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        flush_with_constraints()
        self.registration_url = f'/api/{API_VERSION}/registration/'

    def test_registration(self):
        data = {
            'username': USERNAME_FOR_TESTS,
            'password': PASSWORD_FOR_TESTS
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginTestCase(APITestCase):
    def setUp(self):
        flush_with_constraints()
        self.registration_url = f'/api/{API_VERSION}/registration/'
        self.login_url = f'/api/{API_VERSION}/login/'

        AlarmScenario.objects.get_or_create(
            id=1,
            defaults={
                'name': 'Default Scenario',
                'play_music': False,
                'notify_contact': False,
                'notify_therapist': False
            }
        )

        data = {
            'username': USERNAME_FOR_TESTS,
            'password': PASSWORD_FOR_TESTS
        }
        self.client.post(self.registration_url, data, format='json')

    def test_login(self):
        data = {
            'username': USERNAME_FOR_TESTS,
            'password': PASSWORD_FOR_TESTS
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)


@override_settings(DEBUG=True)
class TestEditUserinfo(APITestCase):
    def setUp(self):
        super().setUp()

        flush_with_constraints()
        post_save.disconnect(receiver=create_user_info, sender=User)
        post_migrate.disconnect(receiver=create_music, dispatch_uid="create_music_post_migrate")

        self.registration_url = f'/api/{API_VERSION}/registration/'
        self.login_url = f'/api/{API_VERSION}/login/'

        registration_for_tests(self.client, self.registration_url)
        self.user = User.objects.get(username=USERNAME_FOR_TESTS)

        self.edit_userinfo_url = f'/api/{API_VERSION}/edit_userinfo/{self.user.id}/'

        login_response = self.client.post(
            self.login_url,
            {'username': USERNAME_FOR_TESTS, 'password': PASSWORD_FOR_TESTS},
            format='json'
        )
        self.token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_edit(self):
        data = {
            'age': 25,
            'military_status': True,
            'ptsd_level': 1,
            'preferred_music': 1,
            'emergency_contact': 1,
            'therapist_contact': 1,
            'scenario': 1
        }

        response = self.client.patch(self.edit_userinfo_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['age'], 25)
        self.assertEqual(response.data['military_status'], True)
