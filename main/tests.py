from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from DjangoProject.settings import API_VERSION, PASSWORD_FOR_TESTS
from django.apps import apps
from main import models
from django.apps import apps


class RegistrationTestCase(APITestCase):
    def __init__(self):
        self.registration_url = None

    def setUp(self):
        self.registration_url = f'/api/{API_VERSION}/registration/'
        for model in apps.get_models():
            model.objects.all().delete()

    def test_registration(self):
        data = {
            'username': 'testuser',
            'password': PASSWORD_FOR_TESTS
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)