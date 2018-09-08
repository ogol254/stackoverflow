"""
This module tests the authentication endpoint
Authored by: ogol
"""
import unittest
import json
import string
from random import choice, randint

# local imports
from ... import create_app
from ...database import destroy
from ...database import _init_db


class AuthTest(unittest.TestCase):
    """This class collects all the test cases for the users"""

    def setUp(self):
        """Performs variable definition and app initialization"""
        self.app = create_app('testing')
        self.client = self.app.test_client()

        self.user = {
            "first_name": "ugali",
            "last_name": "mayai",
            "email": "testemail@gmail.com",
            "username": "testuser",
            "password": "password"
        }
        self.error_msg = "The path accessed / resource requested cannot be found, please check"

        with self.app.app_context():
            self.db = _init_db()

    def post_data(self, path='/api/v2/auth/signup', data={}):
        """This function performs a POST request using the testing client"""
        if not data:
            data = self.user
        result = self.client.post(path, data=json.dumps(data),
                                  content_type='application/json')
        return result

    def get_data(self, path):
        """This function performs a GET request to a given path
            using the testing client
        """
        result = self.client.get(path)
        return result

    def test_sign_up_user(self):
        """Test that a new user can sign up using a POST request
        """
        new_user = self.post_data(data=self.user)
        # test that the server responds with the correct status code
        self.assertEqual(new_user.status_code, 201)
        username = new_user.json['username']
        self.assertEqual(self.user['username'], username)
        self.assertTrue(new_user.json['AuthToken'])
        self.assertTrue(new_user.json['message'])

    def test_error_messages(self):
        """Test that the endpoint responds with the correct error message"""
        empty_req = self.client.post("/api/v2/auth/signup", data={})
        self.assertEqual(empty_req.status_code, 400)
        bad_data = self.user
        del bad_data['first_name']
        empty_params = self.client.post("/api/v2/auth/signup", data=bad_data)
        self.assertEqual(empty_params.status_code, 400)
        empty_req = self.client.post("/api/v2/auth/login", data={"": ""})
        self.assertEqual(empty_req.status_code, 400)
        bad_data = {
            "username": "",
            "password": "pass"
        }
        empty_params = self.client.post("/api/v2/auth/signup", data=bad_data)
        self.assertEqual(empty_params.status_code, 400)

    def test_user_login(self):
        """Test that a user can login using a POST request"""
        self.post_data(data=self.user)
        payload = dict(
            username=self.user['username'],
            password=self.user['password']
        )
        # attempt to log in
        login = self.post_data('/api/v2/auth/login', data=payload)
        self.assertEqual(login.json['message'], 'success')
        self.assertTrue(login.json['AuthToken'])

    def test_user_logout(self):
        """Test that the user can logout using a POST request"""
        new_user = self.post_data().json
        path = "/api/v2/auth/logout"
        token = new_user['AuthToken']
        headers = {"Authorization": "Bearer {}".format(token)}
        logout = self.client.post(path=path,
                                  headers=headers,
                                  content_type="application/json")
        self.assertEqual(logout.status_code, 200)
        logout_again = self.client.post(path=path,
                                        headers=headers,
                                        content_type="application/json")
        self.assertEqual(logout_again.status_code, 401)

    def test_an_unregistered_user(self):
        """Test that an unregistered user cannot log in"""
        # generate random username and password
        un_user = {
            "username": "".join(choice(
                                string.ascii_letters) for x in range(randint(7, 10))),
            "passsword": "".join(choice(
                string.ascii_letters) for x in range(randint(7, 10))),
        }
        # attempt to log in
        login = self.post_data('/api/v2/auth/login', data=un_user)
        self.assertEqual(login.status_code, 400)

    def tearDown(self):
        """This function destroys objests created during the test run"""

        with self.app.app_context():
            destroy()
            self.db.close()


if __name__ == "__main__":
    unittest.main()
