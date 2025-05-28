from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from main.models import UserInfo
from event.models import AlarmScenario
from django.urls import reverse

class EndpointTests(TestCase):
    def setUp(self):
        # Create a test user
        self.username = 'testuser'
        self.password = 'testpassword'
        self.email = 'test@example.com'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email
        )

        # Create a UserInfo object for the user
        self.user_info = UserInfo.objects.get(user=self.user)

        # Create a scenario
        self.scenario = AlarmScenario.objects.create(
            name='Test Scenario',
            play_music=True,
            notify_contact=False,
            notify_therapist=False
        )

        # Assign the scenario to the user
        self.user_info.scenario = self.scenario
        self.user_info.save()

        # Set up the API client
        self.client = APIClient()

        # URLs
        self.registration_url = reverse('main:registration')
        self.login_url = reverse('main:login')
        self.trigger_url = reverse('event:alarm', args=[self.user.id])

    def test_registration(self):
        """Test user registration"""
        # Delete the existing user to avoid conflicts
        User.objects.all().delete()

        data = {
            'username': self.username,
            'password': self.password,
            'email': self.email
        }
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(UserInfo.objects.count(), 1)

    def test_login(self):
        """Test user login"""
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_trigger(self):
        """Test trigger endpoint"""
        # Login to get the token
        login_data = {
            'username': self.username,
            'password': self.password
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        token = login_response.data['token']

        # Set the authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        # Call the trigger endpoint
        response = self.client.get(self.trigger_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['scenario'], self.scenario.name)
