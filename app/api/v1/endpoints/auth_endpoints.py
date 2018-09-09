"""
This module collects the endpoints for the authentication resource
"""
import json
import re
import string

# third party imports
from flask_restplus import Resource
from flask import request, jsonify
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized, Forbidden
from werkzeug.security import generate_password_hash, check_password_hash

# local imports
from ..utils.serializers import UserDTO
from ..models.user_model import UserModel

api = UserDTO().api
_user = UserDTO().user
_n_user = UserDTO().n_user
_n_user_resp = UserDTO().n_user_resp
_user_resp = UserDTO().user_resp
_logout_user_resp = UserDTO().user_logout


def _validate_user(user):
    """This function validates the user input and rejects or accepts it"""
    for key, value in user.items():
        # ensure keys have values
        if not value:
            raise BadRequest("{} is lacking. It is a required field".format(key))
        # validate length
        if key == "username" or key == "password":
            if len(value) < 5:
                raise BadRequest("The {} provided is too short".format(key))
            elif len(value) > 15:
                raise BadRequest("The {} provided is too long".format(key))
        if key == "first_name" or key == "last_name" or key == "username":
            for i in value:
                if i not in string.ascii_letters:
                    raise BadRequest("{} cannot have non-alphabetic characters.".format(key))


@api.route("/signup/")
class AuthSignup(Resource):
    """This class collects the methods for the auth/signup method"""
    docu_string = "This endpoint allows an unregistered user to sign up."

    @api.doc(docu_string)
    @api.expect(_n_user, validate=True)
    @api.marshal_with(_n_user_resp, code=201)
    def post(self):
        """This endpoint allows an unregistered user to sign up."""
        req_data = request.data.decode().replace("'", '"')
        if not req_data:
            raise BadRequest("Provide data in the request")
        user_details = json.loads(req_data)
        try:
            username = user_details['username'].strip()
            first_name = user_details['first_name'].strip()
            last_name = user_details['last_name'].strip()
            email = user_details['email'].strip()
            password = user_details['password'].strip()
            if not re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                            email):
                raise BadRequest("The email provided is invalid")
        except (KeyError, IndexError) as e:
            raise BadRequest
        user = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }
        _validate_user(user)
        user_model = UserModel(**user)
        try:
            saved = user_model.save_user()
            if not saved:
                raise ValueError
        except ValueError:
            raise Forbidden("The username already exists")
        user_id = saved
        token = user_model.encode_auth_token(user_id)
        resp = {
            "message": "User signed up successfully",
            "AuthToken": "{}".format(token.decode('utf-8')),
            "username": username,
            "user_id": "{}".format(user_id)
        }
        user_model.close_db()
        return resp, 201


@api.route("/login/")
class AuthLogin(Resource):
    """This class collects the methods for the auth/login endpoint"""

    docu_string = "This endpoint accepts POST requests to allow a registered user to log in."

    @api.doc(docu_string)
    @api.expect(_user, validate=True)
    @api.marshal_with(_user_resp, code=200)
    def post(self):
        """This endpoint accepts POST requests to allow a registered user to log in."""
        req_data = json.loads(request.data.decode().replace("'", '"'))
        login_details = {
            "username": req_data['username'],
            "password": req_data['password']
        }
        _validate_user(login_details)
        # locate user in db
        user = UserModel(**login_details)
        record = user.get_user_by_username(login_details["username"])
        if not record:
            raise Unauthorized('Your details were not found, please sign up')
        user_id, fname, lname, pwordhash, date_created = record
        if not check_password_hash(pwordhash, login_details["password"]):
            raise Unauthorized("The username or password is incorrect")
        name = "{}, {}".format(lname, fname)
        token = user.encode_auth_token(int(user_id))
        resp = dict(
            message="success",
            AuthToken=token.decode('utf-8'),
            name=name,
            date_created=date_created
        )
        return resp, 200


@api.route('/logout')
class AuthLogout(Resource):
    """This class collects the methods for the questions endpoint"""

    docu_string = "This endpoint allows a registered user to logout."

    @api.doc(docu_string)
    @api.marshal_with(_logout_user_resp, code=200)
    def post(self):
        """This endpoint allows a registered user to logout."""
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            raise BadRequest(
                "No authorization header provided. This resource is secured.")
        auth_token = auth_header.split(" ")[1]
        response = UserModel().decode_auth_token(auth_token)
        if isinstance(response, str):
            # token is either invalid or expired
            raise Unauthorized(
                "You are not authorized to access this resource. %s" % (response))
        else:
            # the token decoded succesfully
            # logout the user
            user_token = UserModel().logout_user(auth_token)
            resp = dict()
            return {"message": "logout successful. {}".format(user_token)}, 200
