import unittest
from unittest.mock import patch

from flask import json
from flask_migrate import upgrade

from app import create_app


class MockedResponse:
    def __init__(self, status_code, text):
        self.statuscode = status_code
        self.text = text
        self.headers = {'Authorization':'Bearer Token'}

    def json(self):
        return json.loads(self.text)


class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config.TestConfig')
        self.app.testing = True
        self.app_ctxt = self.app.app_context()
        self.app_ctxt.push()
        upgrade()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_ctxt.pop()

    @patch('app.api.auth.login')
    def test_login_with_valid_user(self, mock_get):
        mock_get.return_value = MockedResponse(200, json.dumps({'user_id': '', 'access_token': 'Token', 'refresh_token': 'Token'}))

        response = self.client.post('/api/auth/login', json={"email": "test@example.com", "password": "test"})

        self.assertEqual(response.status_code, 200)

    @patch('app.api.auth.signup')
    def test_signup(self, mock_get):
        mock_get.return_value = MockedResponse(302, json.dumps({'user_id': ''}))

        response = self.client.post('/api/auth/signup', json={"email": "test@example.com", "password": "test"})

        self.assertEqual(response.status_code, 200)


    @patch('app.api.auth.validate_token')
    def test_validate_token_with_invalid_token(self, mock_get):
        mock_get.return_value = MockedResponse(200, json.dumps({"message": "Token is invalid"}))

        headers = {'Authorization':'Bearer {}'}
        response = self.client.get('/api/auth/tokens/validate', headers=headers)

        self.assertEqual(response.status_code, 422)
