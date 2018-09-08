"""
This module collects the views for the answers resource
"""
import json

# third party imports
from flask_restplus import Resource
from flask import request, jsonify
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden

from ..models.user_model import UserModel
from ..models.question_model import QuestionModel
from ..models.answer_model import AnswerModel

from ..utils.serializers import AnswerDTO

api = AnswerDTO().api
_n_answer = AnswerDTO().n_answer
_n_answer_resp = AnswerDTO().n_answer_resp
_edit_answer_resp = AnswerDTO().edit_answer_resp
_vote_ans = AnswerDTO().votes
_vote_resp = AnswerDTO.vote_answer_resp


def _validate_input(req):
    """This function validates the user input and rejects or accepts it"""
    for key, value in req.items():
        # ensure keys have values
        if not value:
            raise BadRequest("{} is lacking. It is a required field".format(key))
        elif len(value) < 10:
            raise BadRequest("The {} is too short. Please add more content.".format(key))


def _locate_question_and_answer(question_id, answer_id):
    """Check if the question id and answer id passed in the url exist in the db"""
    answers = AnswerModel()
    find_qstn = QuestionModel().get_item_by_id(question_id)
    find_ans = answers.get_item_by_id(answer_id)
    if find_qstn == "Not Found" or find_ans == "Not Found":
        # the question or answer was not found
        raise NotFound("the question or answer was not found")


@api.route('/')
class Answers(Resource):
    """This class collects the methods for the answers endpoint"""

    docu_string = "This endpoint handles POST requests to the answers resource"

    @api.doc(docu_string)
    @api.expect(_n_answer, validate=True)
    @api.marshal_with(_n_answer_resp, code=201)
    def post(self, question_id):
        """This endpoint handles post requests to enable a user to post an answer to a question"""
        auth_header = request.headers.get('Authorization')
        if not auth_header or not request.data:
            raise BadRequest("The request is malformed. Attach missing fields")
        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if not isinstance(response, str):
            # the token decoded succesfully
            user_id = response
            req_data = json.loads(request.data.decode().replace("'", '"'))
            _validate_input(req_data)
            text = req_data['text']
            # save answer in db
            answer = AnswerModel(int(question_id), int(user_id), text)
            check = answer.check_text_exists(text)
            if isinstance(check, int):
                # asnwer exists in the db
                raise Forbidden("The answer exists in the database.")
            answer_id = int(answer.save_answer())
            answer.close_db()
            resp = {
                "message": "success",
                "text": text,
                "answer_id": answer_id
            }
            return resp, 201
        else:
            # token is either invalid or expired
            raise Unauthorized
