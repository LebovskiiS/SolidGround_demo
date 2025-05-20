from rest_framework.test import APITestCase
from rest_framework import status
from django.core.management import call_command
from event.models import AlarmScenario
from DjangoProject.settings import API_VERSION, PASSWORD_FOR_TESTS, USERNAME_FOR_TESTS

def registratiopn_for_tests(client, registration_url):
    call_command('flush', '--noinput')
    data = {
        'username': USERNAME_FOR_TESTS,
        'password': PASSWORD_FOR_TESTS
    }
    response = client.post(registration_url, data, format='json')


# class TriggerAlarmTestCase(APITestCase):
#     def setUp(self):
#         self.registration_url = f'/api/{API_VERSION}/registration/'
#         self.login_url = f'/api/{API_VERSION}/login/'
#         self.trigger_alarm_url = f'/api/{API_VERSION}/trigger_alarm/'
#         registratiopn_for_tests(self.client, self.registration_url)