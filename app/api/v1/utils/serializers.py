"""
This module collects all the Data Transfer Objects for the API
"""
from flask_restplus import Namespace, fields


class UserDTO(object):
    """User Data Transfer Object"""
    api = Namespace('auth', description='user authentication and signup resources')
    n_user = api.model('new user request', {
        'first_name': fields.String(required=True, description="user's first name"),
        'last_name': fields.String(required=True, description="user's last name"),
        'username': fields.String(required=True, description="user's username"),
        'email': fields.String(required=True, description="user's email address"),
        'password': fields.String(required=True, description="user's password")
    })
    n_user_resp = api.model('response to signup', {
        'message': fields.String(required=True, description="success or fail message"),
        'AuthToken': fields.String(required=True, description="authentication token"),
        'username': fields.String(required=True, description="user's username"),
        'user_id': fields.String(required=True, description="user's id")
    })
    user_resp = api.model('response to login', {
        'message': fields.String(required=True, description="success or fail message"),
        'AuthToken': fields.String(required=True, description="authentication token"),
        'name': fields.String(required=True, description="user's username"),
        'date_created': fields.String(required=True, description="user's id")
    })
    user = api.model('login request', {
        'username': fields.String(required=True, description="user's username"),
        'password': fields.String(required=True, description="user's password")
    })
    user_logout = api.model('logout request', {
        'message': fields.String(required=True, description="success message")
    })


class QuestionUserDTO(object):
    """Questions by user Data Transfer Object"""
    api = Namespace('questions by a user', description='questions asked by a user')
    questions_by_user_resp = api.model('questions by a user', {
        "question_id": fields.Integer(required=True, description="identifier of the question"),
        "username": fields.String(required=True, description="the username of the user who asked the question"),
        "text": fields.String(required=True, description="the title of the question"),
        "date_created": fields.String(required=True, description="the date the question was created")
    })
    get_by_user_resp = api.model('response to retrieving questions by username', {
        'message': fields.String(required=True, description="success or fail message"),
        'username': fields.String(required=True, description="username of the one who asked the questions"),
        'questions': fields.List(fields.Nested(questions_by_user_resp), required=False, description="list of all the questions")
    })


class QuestionDTO(object):
    """Question Data Transfer Object"""
    api = Namespace('question', description='question resource')
    n_question = api.model('new question', {
        'text': fields.String(required=True, description="the title of the question"),
        'description': fields.String(required=True, description="a description of the question")
    })
    n_question_resp = api.model('response to a new question', {
        'message': fields.String(required=True, description="success or fail message"),
        'text': fields.String(required=True, description="title of the created question"),
        'asked_by': fields.String(required=True, description="user's username"),
        'question_id': fields.String(required=True, description="question's id")
    })
    question_list_response = api.model('list of questions', {
        "question_id": fields.String(required=True, description="question's id"),
        "user_id": fields.String(required=True, description="the id of the user who asked the question"),
        "text": fields.String(required=True, description="question's title"),
        "description": fields.String(required=True, description="a description of the question"),
        "date_created": fields.String(required=True, description="date the question was created")
    })
    get_questions_resp = api.model('response to get questions', {
        'message': fields.String(required=True, description="success or fail message"),
        'questions': fields.List(fields.Nested(question_list_response), required=True, description="list of all the questions")
    })
    get_edit_resp = api.model('response to an edit question request', {
        'message': fields.String(required=True, description="success or fail message"),
        'text': fields.String(required=True, description="The string of the edited question")
    })
    delete_resp = api.model('response to delete question', {
        'message': fields.String(required=True, description="success or fail message"),
        'description': fields.String(required=True, description="The string of the edited question")
    })
    answer_by_question_id = api.model('answers to a question', {
        "answer_id": fields.Integer(required=True, description="the identifier of the answer"),
        "question_id": fields.Integer(required=True, description="identifier of the question"),
        "username": fields.String(required=True, description="the username of the user who asked the question"),
        "text": fields.String(required=True, description="the title of the answer"),
        "date_created": fields.String(required=True, description="the date the answer was created"),
        "up_votes": fields.Integer(required=True, description="upvotes given to an answer"),
        "user_preferred": fields.Boolean(required=True, description="whether the answer is preferred by the user who asked the question")
    })
    get_question_resp = api.model('response to get questions', {
        'username': fields.String(required=True, description="username of the one who asked the question"),
        'text': fields.String(required=True, description="title of the created question"),
        'description': fields.String(required=True, description="a description of the question"),
        'date_created': fields.String(required=True, description="user's username"),
        'answers': fields.List(fields.Nested(answer_by_question_id), required=False, description="question's answers")
    })
    get_most_answered = api.model('response to get questions', {
        'username': fields.String(required=True, description="username of the one who asked the question"),
        "question_id": fields.Integer(required=True, description="identifier of the question"),
        "number": fields.Integer(required=True, description="Number of answers the question has"),
        'text': fields.String(required=True, description="title of the created question"),
        'description': fields.String(required=True, description="a description of the question"),
        'date_created': fields.String(required=True, description="user's username"),
        'answers': fields.List(fields.Nested(answer_by_question_id), required=False, description="question's answers")
    })


class AnswerDTO(object):
    """Data transfer object for the answers resource"""
    api = Namespace('Answer endpoint', description='answers resource')
    n_answer = api.model('createanswer', {
        "text": fields.String(required=True, description="the title of the answer")
    })
    n_answer_resp = api.model('response to a new answer', {
        "message": fields.String(required=True, description="request status"),
        "text": fields.String(required=True, description="the title of the answer"),
        "answer_id": fields.Integer(required=True, description="the id of the answer")
    })
    edit_answer_resp = api.model('response to editing or marking an answer as preferred', {
        "message": fields.String(required=True, description="request status"),
        "description": fields.String(required=True, description="request status"),
        "value": fields.String(required=True, description="the edit response")
    })
    votes = api.model('the request structure for a up/downvote', {
        "vote": fields.String(required=True, description="the vote value")
    })
    vote_answer_resp = api.model('response to editing or marking an answer as preferred', {
        "message": fields.String(required=True, description="request status"),
        "description": fields.String(required=True, description="request status"),
        "new_votes": fields.String(required=True, description="the new value for upvotes field")
    })
