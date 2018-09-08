"""
This module collects the views for the questions resource
"""
import json
import re

# third party imports
from flask_restplus import Resource
from flask import request, jsonify
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden

# local imports
from ..models.user_model import UserModel
from ..models.question_model import QuestionModel
from ..models.answer_model import AnswerModel

from ..utils.serializers import QuestionDTO, QuestionUserDTO

api = QuestionDTO().api
uapi = QuestionUserDTO.api
_n_question = QuestionDTO().n_question
_n_question_resp = QuestionDTO().n_question_resp
_get_questions_resp = QuestionDTO().get_questions_resp
_get_question_resp = QuestionDTO().get_question_resp
_get_edit_resp = QuestionDTO().get_edit_resp
_delete_resp = QuestionDTO().delete_resp
_get_most_answered = QuestionDTO().get_most_answered
_get_by_user_resp = QuestionUserDTO().get_by_user_resp


def _validate_input(req):
    """This function validates the user input and rejects or accepts it"""
    for key, value in req.items():
        # ensure keys have values
        if not value:
            raise BadRequest("{} is lacking. It is a required field".format(key))
        elif len(value) < 10:
            raise BadRequest("The {} is too short. Please add more content.".format(key))


@api.route('/')
class Questions(Resource):
    """This class collects the methods for the questions endpoint"""

    docu_string = "This endpoint allows a registered user to post a question."

    @api.doc(docu_string)
    @api.expect(_n_question, validate=True)
    @api.marshal_with(_n_question_resp, code=201)
    def post(self):
        """This endpoint allows a registered user to post a question."""
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise BadRequest("No authorization header provided. This resource is secured.")
        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if not isinstance(response, str):
            # the token decoded succesfully
            user_id = response
            if not request.data:
                raise BadRequest("The request body is empty, restructure.")
            req_data = json.loads(request.data.decode().replace("'", '"'))
            text = req_data['text']
            description = req_data['description']
            data = dict(text=text, description=description)
            # save question in db
            _validate_input(data)
            question = QuestionModel(int(user_id), text, description)
            check = question.check_text_exists(text)
            if isinstance(check, int):
                # question exists in the db
                raise Forbidden("The question exists in the database.")
            question_id = question.save_question()
            username = question.get_username_by_id(int(user_id))
            question.close_db()
            resp = dict(message="success",
                        text=text,
                        asked_by=username,
                        question_id=str(question_id))

            return resp, 201
        else:
            # token is either invalid or expired
            raise Unauthorized("You are not authorized to access this resource.")

    docu_string = "This endpoint allows a registered user to post a question."

    @api.doc(docu_string)
    @api.marshal_with(_get_questions_resp, code=200)
    def get(self):
        """This endpoint allows a registered user to post a question."""
        # get questions from db
        questions = QuestionModel().get_all()
        resp = {
            "message": "success",
            "questions": questions
        }
        return resp, 200


@api.route('/<int:question_id>')
class GetQuestion(Resource):
    """This class collects the views for a particular question"""

    docu_string = "This endpoint allows a user to get all the details to a question."

    @api.doc(docu_string)
    @api.marshal_with(_get_question_resp, code=200)
    def get(self, question_id):
        """Returns a question and all it's answers
        This endpoint allows a user to get all the details to a question."""
        # no auth required
        question = QuestionModel().get_item_by_id(int(question_id))
        if not question:
            # question was not found
            raise NotFound("The question was not found in the database.")
        else:
            # find it's answers
            answers = AnswerModel().get_answers_by_question_id(int(question_id))
            question_id, user_id, text, description, date_created = question
            user = UserModel().get_username_by_id(int(user_id))  # returns the username
            resp = dict(username=user,
                        text=text,
                        description=description,
                        date_created=date_created,
                        answers=answers)
            return resp, 200

    docu_string = "This endpoint allows a user to edit the details of a question."

    @api.doc(docu_string)
    @api.expect(validate=False)
    @api.marshal_with(_get_edit_resp, code=200)
    def put(self, question_id):
        """This function edits a question, given the id"""
        auth_header = request.headers.get('Authorization')
        if not auth_header or len(auth_header) < 8 or " " not in auth_header:
            raise BadRequest("Authorization not provided or inadequate.")
        auth_token = auth_header.split(" ")[1]
        request_id = UserModel().decode_auth_token(auth_token)
        if isinstance(request_id, str):
            raise Unauthorized("You are not authorized to access this resource.")
        else:
            # confirm user request
            update = request.get_json()
            _validate_input(update)
            questions = QuestionModel()
            question = questions.get_item_by_id(int(question_id))
            if question == "Not found":
                raise NotFound("The question was not found in the database")
            question_id = question[0]
            user_id = question[1]
            if int(user_id) == int(request_id):
                # update question
                for field, data in update.items():
                    questions.update_item(field=field, data=data,
                                          item_id=int(question_id))
            else:
                raise Forbidden("You are not allowed to edit the question")
            resp = {"message": "success", "text": str(update)}
            return resp, 200

    docu_string = "This endpoint allows a user to delete a question."

    @api.doc(docu_string)
    @api.marshal_with(_delete_resp, code=202)
    def delete(self, question_id):
        """This function deletes a question, given the id"""
        auth_header = request.headers.get('Authorization')
        if not auth_header or len(auth_header) < 8 or " " not in auth_header:
            raise BadRequest("Authorization not provided or inadequate.")
        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if isinstance(response, str):
            raise Unauthorized("You do not have the authorization to delete the question")
        else:
            # user is authorized
            questions = QuestionModel()
            question = questions.get_item_by_id(int(question_id))
            if question == "Not found":
                raise NotFound("The question was not located in the database")
            question_id = question[0]
            user_id = question[1]
            # check if user ids match
            if int(user_id) == int(response):
                # delete question
                questions.delete_item(int(question_id), foreign_key="answers")
            else:
                raise Forbidden("You are not allowed to delete the question")
            resp = {"message": "success",
                    "description": "question deleted succesfully"}
            return resp, 202


@uapi.route("/")
class GetUserQuestion(Resource):
    """question views associated with users"""

    docu_string = "This endpoint allows a user to get all the questions asked by a user"

    @uapi.doc(docu_string)
    @uapi.marshal_with(_get_by_user_resp, code=200)
    def get(self, username):
        """returns all the questions associated with a particular user"""
        """This function deletes a question, given the id"""
        # import pdb;pdb.set_trace()
        users = UserModel()
        try:
            user_id = users.get_user_by_username(username)
            if not user_id:
                raise ValueError
        except ValueError:
            raise NotFound("The username provided does not exist")
        user_id = user_id[0]
        quest = QuestionModel()
        questions = quest.get_items_by_id(item='user',
                                          item_id=int(user_id))
        list_of_questions = []
        if not questions:
            # no question was not found
            raise NotFound("The user has no questions in the database")
        if not isinstance(questions, list):
            list_of_questions.append(questions)
        else:
            list_of_questions = questions[:]
        resp = {
            "message": "success",
            "username": username,
            "questions": questions
        }
        return resp, 200
