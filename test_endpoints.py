import requests
import json

# Base URL
BASE_URL = 'http://localhost:8000/api/v1'

# Test user credentials
USERNAME = 'testuser'
PASSWORD = 'YOUR_TEST_PASSWORD_HERE'
EMAIL = 'test@example.com'

# Registration
def test_registration():
    url = f'{BASE_URL}/user/registration/'
    data = {
        'username': USERNAME,
        'password': PASSWORD,
        'email': EMAIL
    }
    response = requests.post(url, json=data)
    print(f'Registration status code: {response.status_code}')
    print(f'Registration response: {response.text}')
    return response.status_code == 201

# Login
def test_login():
    url = f'{BASE_URL}/user/login/'
    data = {
        'username': USERNAME,
        'password': PASSWORD
    }
    response = requests.post(url, json=data)
    print(f'Login status code: {response.status_code}')
    print(f'Login response: {response.text}')

    if response.status_code == 200:
        return response.json().get('token')
    return None

# Trigger
def test_trigger(token, user_id=1):
    url = f'{BASE_URL}/event/trigger/{user_id}/'
    headers = {
        'Authorization': f'Token {token}'
    }
    response = requests.get(url, headers=headers)
    print(f'Trigger status code: {response.status_code}')
    print(f'Trigger response: {response.text}')
    return response.status_code == 200

# Main test function
def run_tests():
    # Test registration
    if not test_registration():
        print('Registration test failed')
        return

    # Test login
    token = test_login()
    if not token:
        print('Login test failed')
        return

    # Test trigger
    if not test_trigger(token):
        print('Trigger test failed')
        return

    print('All tests passed!')

if __name__ == '__main__':
    run_tests()
