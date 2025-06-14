from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from event.models import AlarmScenario
from DjangoProject.settings import API_VERSION, PASSWORD_FOR_TESTS, USERNAME_FOR_TESTS
from main.exceptions import RegistrationInTestsError
from django.db import connection
from django.test import override_settings
from django.db.models.signals import post_save, post_migrate
from main.signals import create_user_info







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
            'password': PASSWORD_FOR_TESTS,
            'email': 'test@example.com'
        }
        response = client.post(registration_url, data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            raise RegistrationInTestsError(f"User registration failed. Status code: {response.status_code}, Response: {response.content}")
    except Exception as e:
        print(f"Registration failed: {e}")
        raise RegistrationInTestsError(str(e))


class RegistrationTestCase(APITestCase):
    def setUp(self):
        super().setUp()
        flush_with_constraints()
        self.registration_url = f'/api/{API_VERSION}/user/registration/'

    def test_registration(self):
        data = {
            'username': USERNAME_FOR_TESTS,
            'password': PASSWORD_FOR_TESTS,
            'email': 'test@example.com'
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginTestCase(APITestCase):
    def setUp(self):
        flush_with_constraints()
        self.registration_url = f'/api/{API_VERSION}/user/registration/'
        self.login_url = f'/api/{API_VERSION}/user/login/'

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
            'password': PASSWORD_FOR_TESTS,
            'email': 'test@example.com'
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
class TestGetUserinfo(APITestCase):
    def setUp(self):
        super().setUp()

        flush_with_constraints()
        post_save.disconnect(receiver=create_user_info, sender=User)

        self.registration_url = f'/api/{API_VERSION}/user/registration/'
        self.login_url = f'/api/{API_VERSION}/user/login/'

        registration_for_tests(self.client, self.registration_url)
        self.user = User.objects.get(username=USERNAME_FOR_TESTS)

        self.userinfo_url = f'/api/{API_VERSION}/user/1/' # Using user ID 1

        login_response = self.client.post(
            self.login_url,
            {'username': USERNAME_FOR_TESTS, 'password': PASSWORD_FOR_TESTS},
            format='json'
        )
        self.token = login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_get_userinfo(self):
        response = self.client.get(self.userinfo_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('scenario', response.data)
