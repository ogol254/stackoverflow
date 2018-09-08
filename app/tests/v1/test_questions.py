"""
This module tests the questions end point
"""
import unittest
import json
import string
from random import choice, randint

# local imports
from ... import create_app

from ...database import _init_db
from ...database import destroy

##from ...api.v1.models.user_model import UserModel



class TestQuestions(unittest.TestCase):
    """This class collects all the test cases for the questions"""
    def create_user(self):
        """create a fictitious user"""
        username = "".join(choice(
                           string.ascii_letters) for x in range (randint(7,10)))
        params = {
                "first_name":"ugali",
                "last_name":"mayai",
                "email":"ugalimayai@gmail.com",
                "username":username,
                "password":"password"
            }
        path = "/api/v1/auth/signup"
        user = self.client.post(path,
                                data=json.dumps(params),
                                content_type="application/json")
        
        user_id = user.json['user_id']
        auth_token = user.json['AuthToken']
        return int(user_id), auth_token

    def setUp(self):
        """Performs variable definition and app initialization"""
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.question = {
            "text":"".join(choice(
                           string.ascii_letters) for x in range (randint(20,25))),
            "description":"I am looking for the fastest programming language in terms\
                            of memory management for a very high performance project."
        }
        with self.app.app_context():
            self.db = _init_db()

    def post_data(self, path='/api/v1/questions', auth_token=2, data={}, headers=0):
        """This function performs a POST request using the testing client"""
        if not data:
            data = self.question
        if auth_token is 2:
            user = self.create_user()
            auth_token = user[1]
        if not headers:
            headers = {"Authorization":"Bearer {}".format(auth_token)}
        result = self.client.post(path, data=json.dumps(data),
                                  headers=headers,
                                  content_type='application/json')
        return result

    def get_data(self, path='/api/v1/questions'):
        """This function performs a GET request to a given path
            using the testing client
        """
        result = self.client.get(path)
        return result

    def test_post_question(self):
        """Test that a user can post a question
        """
        new_question = self.post_data()
        # test that the server responds with the correct status code
        self.assertEqual(new_question.status_code, 201)
        self.assertTrue(new_question.json['message'])
        self.assertTrue(new_question.json['question_id'])

        
    def test_error_messages(self):
        """Test that the endpoint responds with the correct error message"""
        auth_token = self.create_user()[1]
        empty_req = self.client.post("/api/v1/questions",
                                     headers=dict(Authorization="Bearer {}".format(auth_token)),
                                     data={})
        self.assertEqual(empty_req.status_code, 400)
        bad_data = self.question
        del bad_data['text']
        empty_params = self.post_data(data=bad_data)
        self.assertEqual(empty_params.status_code, 400)
        empty_req = self.post_data(data={"":""})
        self.assertEqual(empty_req.status_code, 400)
        bad_data = {
            "user_id":"",
            "textsss":"What is the fastest programming language and why?",
            "description":"Description"
        }
        bad_req = self.post_data(data=bad_data)
        self.assertEqual(bad_req.status_code, 400)
    
    def test_unauthorized_request(self):
        """Test that the endpoint rejects unauthorized requests"""
        # test false token
        false_token = self.post_data(headers=dict(Authorization="Bearer wrongtoken"))
        self.assertEqual(false_token.status_code, 401)
        # test correct token
        correct_token = self.post_data()
        self.assertEqual(correct_token.status_code, 201)

    def test_get_questions(self):
        """Test that the api can respond with a list of questions"""
        new_question = self.post_data()
        questions = self.get_data().json
        self.assertEqual(questions['message'], 'success')
        self.assertIn(new_question.json['text'], str(questions['questions']))

    def test_get_questions_associated_to_user(self):
        """Test that the API responds with all the questions of a particular user"""
        user_id, auth_token = self.create_user()
        question = self.post_data(headers={"Authorization":"Bearer {}".format(auth_token)})
        username = question.json['asked_by']
        path = "/api/v1/questions/{}".format(username)
        req = self.client.get(path=path)
        # import pdb;pdb.set_trace()
        self.assertEqual(req.status_code, 200)
        self.assertEqual(username, req.json["username"])
    
    def test_edit_question(self):
        """Test that a user can edit the text of a question that they've posted"""
        user_id, auth_token = self.create_user()
        question_id = int(self.post_data(auth_token=auth_token).json['question_id'])
        headers = {"Authorization":"Bearer {}".format(auth_token)}
        path  = "/api/v1/questions/{}".format(question_id)
        data = {"text":"edited question"}
        result = self.client.put(path,
                                 headers=headers,
                                 data=json.dumps(data),
                                 content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertIn(data['text'], result.json['text'])

    def test_delete_question(self):
        """Test that a user can delete a question that they have posted"""
        user_id, auth_token = self.create_user()
        question_id = int(self.post_data(auth_token=auth_token).json['question_id'])
        headers = {"Authorization":"Bearer {}".format(auth_token)}
        path  = "/api/v1/questions/{}".format(question_id)
        result = self.client.delete(path,
                                    headers=headers,
                                    content_type='application/json')
        self.assertEqual(result.status_code, 202)
        self.assertEqual(result.json['message'], 'success')

    def test_most_answered(self):
        """Test that the API can respond with the most answered question"""
        auth_token = self.create_user()[1]
        qstn_1 = int(self.post_data(auth_token=auth_token).json['question_id'])
        # post 5 answers to question 1
        path  = "/api/v1/questions/{}/answers".format(qstn_1)
        for x in range(6):
            random_answer ={
            "text":"".join(choice(
                           string.ascii_letters) for x in range (randint(20,25)))
            }
            ans = self.post_data(path=path,
                                 data=random_answer,
                                 auth_token=auth_token)
        path = "/api/v1/questions/answers/most"
        result = self.get_data(path=path)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json["question_id"], qstn_1)

    def tearDown(self):
        """This function destroys items created during the test run"""
        with self.app.app_context():
            destroy()
            self.db.close()

if __name__ == "__main__":
    unittest.main()