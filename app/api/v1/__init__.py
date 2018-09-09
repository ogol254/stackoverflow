"""
This module sets up the users resource
Authored by: Ogol
"""
from flask_restplus import Api
from flask import Blueprint
from werkzeug.exceptions import NotFound

version1 = Blueprint('version1', __name__, url_prefix="/api/v1")

from .endpoints.auth_endpoints import api as auth_ns
from .endpoints.question_endpoints import uapi as question_user_ns
from .endpoints.question_endpoints import api as question_ns
from .endpoints.answer_endpoints import api as answers_ns


api = Api(version1,
          title='Stackoverflow-Lite API',
          version='1.0',
          description="An amateur's simulation of the stackoverflow Q/A system")

api.add_namespace(auth_ns, path="/auth")
api.add_namespace(question_ns, path="/questions")
api.add_namespace(question_user_ns, path="/questions/<username>")
api.add_namespace(answers_ns, path="/questions/<int:question_id>/answers")
