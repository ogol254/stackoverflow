"""
This module tests the answers end point
"""
import unittest
import json
import string
from random import choice, randint

# local imports
from ... import create_app
from ...database import _init_db
from ...database import destroy

#from ...api.v1.models.user_model import UserModel
#from ...api.v1.models.question_model import QuestionModel
#from ...api.v1.models.answer_model import AnswerModel


class TestAnswers(unittest.TestCase):
    """This class collects all the test cases for the questions"""

    def setUp(self):
        """Performs variable definition and app initialization"""
        self.app = create_app("testing")
        self.client = self.app.test_client()

        self.answer = {
            "text": "".join(choice(
                string.ascii_letters) for x in range(randint(16, 20)))
        }

        with self.app.app_context():
            self.db = _init_db()

    def create_user(self):
        """create a fictitious user"""
        username = "".join(choice(
                           string.ascii_letters) for x in range(randint(7, 10)))
        params = {
            "first_name": "ugali",
            "last_name": "mayai",
            "email": "ugalimayai@gmail.com",
            "username": username,
            "password": "password"
        }
        path = "/api/v1/auth/signup"
        user = self.client.post(path,
                                data=json.dumps(params),
                                content_type="application/json")

        user_id = user.json['user_id']
        auth_token = user.json['AuthToken']
        return int(user_id), auth_token

    def create_question(self, user_id=0):
        """This function sets up a test question in the db
        """
        resp = self.create_user()
        if user_id == 0:
            user_id = resp[0]

        params = {
            "user_id": user_id,
            "text": "What is the fastest programming language and why do you think so?",
            "description": "I am looking for the fastest programming language in terms\
                            of memory management for a very high performance project."
        }
        headers = {
            "Authorization": "Bearer {}".format(resp[1]),
            "Content-Type": "application/json"
        }
        path = "/api/v1/questions"
        question = self.client.post(path=path,
                                    data=json.dumps(params),
                                    headers=headers)
        question_id = question.json['question_id']
        return int(question_id), question

    def post_data(self, question_id, auth_token=2, data={}, headers=0):
        """This function performs a POST request using the testing client"""
        if not data:
            data = self.answer
        user = self.create_user()
        user_id = user[0]
        if auth_token is 2:
            auth_token = user[1]
        if not headers:
            headers = {"Authorization": "Bearer {}".format(auth_token)}
        path = "/api/v1/questions/{}/answers".format(int(question_id))
        result = self.client.post(path, data=json.dumps(data),
                                  headers=headers,
                                  content_type='application/json')
        return result

    def test_post_answer(self):
        """Test that a user can post an answer
        """
        user_id = self.create_user()[0]
        question_id = int(self.create_question(user_id)[0])
        new_answer = self.post_data(int(question_id))
        # test that the server responds with the correct status code
        self.assertEqual(new_answer.status_code, 201)
        self.assertTrue(new_answer.json['message'])

    def test_error_messages(self):
        """Test that the endpoint responds with the correct error message"""
        user = self.create_user()
        user_id = user[0]
        question_id = self.create_question(int(user_id))[0]
        path = "/api/v1/questions/{}/answers".format(question_id)
        auth_token = user[1]
        empty_req = self.client.post(path,
                                     headers=dict(Authorization="Bearer {}".format(auth_token)),
                                     data={})
        self.assertEqual(empty_req.status_code, 400)
        empty_req = self.post_data(question_id=question_id, data={"": ""})
        self.assertEqual(empty_req.status_code, 400)

    def test_unauthorized_request(self):
        """Test that the endpoint rejects unauthorized requests"""
        # test false token
        user_id = self.create_user()[0]
        question_id = int(self.create_question(user_id)[0])
        false_token = self.post_data(question_id, headers={"Authorization": "Bearer wrongtoken"})
        self.assertEqual(false_token.status_code, 401)

    def test_edit_answer(self):
        """Test that the author of a particular answer can edit it"""
        user = self.create_user()
        user_id = user[0]  # answer author user id
        question_id = int(self.create_question()[0])
        # token should be encoded with the id of the answer author
        auth_token = user[1]
        new_answer = self.post_data(question_id, auth_token=auth_token).json
        answer_id = int(new_answer['answer_id'])
        headers = {"Authorization": "Bearer {}".format(auth_token)}
        path = "/api/v1/questions/{}/answers/{}".format(question_id,
                                                        answer_id)
        data = {"text": "edited answer"}
        result = self.client.put(path,
                                 headers=headers,
                                 data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json['value'], data['text'])

    def test_upvote_and_downvote(self):
        """Test that an answer can be upvoted or downvoted"""
        user = self.create_user()
        user_id = user[0]  # answer author user id
        question_id = int(self.create_question()[0])
        # token should be encoded with the id of the answer author
        auth_token = user[1]
        new_answer = self.post_data(question_id, auth_token=auth_token).json
        answer_id = int(new_answer['answer_id'])
        headers = {"Authorization": "Bearer {}".format(auth_token)}
        path = "/api/v1/questions/{}/answers/{}/vote".format(question_id,
                                                             answer_id)
        result = self.client.put(path,
                                 headers=headers,
                                 data=json.dumps({"vote": "+1"}),
                                 content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json['new_votes'], "1")
        result = self.client.put(path,
                                 headers=headers,
                                 data=json.dumps({"vote": "-1"}),
                                 content_type='application/json')
        self.assertEqual(result.json['new_votes'], "0")
        # test that the endpoint rejects more than one vote.
        result = self.client.put(path,
                                 headers=headers,
                                 data=json.dumps({"vote": "5"}),
                                 content_type='application/json')
        self.assertEqual(result.status_code, 400)
        self.assertTrue(result.json['message'])

    def tearDown(self):
        """
        This function destroys objests created during the test run
        """
        with self.app.app_context():
            destroy()
            self.db.close()


if __name__ == "__main__":
    unittest.main()
