from rest_framework.test import APITestCase
from rest_framework import status
from django.apps import apps
from DjangoProject.settings import API_VERSION, PASSWORD_FOR_TESTS, USERNAME_FOR_TESTS


class RegistrationTestCase(APITestCase):
    def setUp(self):
        self.registration_url = f'/api/{API_VERSION}/registration/'
        for model in apps.get_models():
            model.objects.all().delete()

    def test_registration(self):
        data = {
            'username': USERNAME_FOR_TESTS,
            'password': PASSWORD_FOR_TESTS
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginTestCase(APITestCase):

    def setUp(self):
        self.registration_url = f'/api/{API_VERSION}/registration/'
        self.login_url = f'/api/{API_VERSION}/login/'
        for model in apps.get_models():
            model.objects.all().delete()
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
