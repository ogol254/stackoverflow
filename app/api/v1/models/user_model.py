"""
This module defines the user model and associated functions
"""
from datetime import datetime, timedelta

import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

# local imports
from .... import create_app
from ....database import init_db
from .base_model import BaseModel


class UserModel(BaseModel):
    """This class encapsulates the functions of the user model"""

    def __init__(self, username="user", first_name="first",
                 last_name="last", password="pass", email="em@ai.l"):
        """initialize the user model"""
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = generate_password_hash(password)
        self.email = email
        self.date_created = datetime.now()
        self.db = init_db()

    def get_user_by_username(self, username):
        """return user from the db given a username"""
        database = self.db
        curr = database.cursor()
        curr.execute(
            """SELECT user_id, first_name, last_name, password, date_created \
            FROM users WHERE username = '%s'""" % (username))
        data = curr.fetchone()
        curr.close()
        return data

    def check_exists(self, username):
        """Check if the records exist"""
        curr = self.db.cursor()
        query = "SELECT username FROM users WHERE username = '%s'" % (username)
        curr.execute(query)
        return curr.fetchone() is not None

    def logout_user(self, token):
        """This function logs out a user by adding thei token to the blacklist table"""
        conn = self.db
        curr = conn.cursor()
        query = """
                INSERT INTO blacklist 
                VALUES (%(tokens)s) RETURNING tokens;
                """
        inputs = {"tokens": token}
        curr.execute(query, inputs)
        blacklisted_token = curr.fetchone()[0]
        conn.commit()
        curr.close()
        return blacklisted_token

    def save_user(self):
        """Add user details to the database"""
        user = {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password
        }
        # check if user exists
        if self.check_exists(user['username']):
            return False
        database = self.db
        curr = database.cursor()
        query = """INSERT INTO users (first_name, last_name, username, email, date_created, password) \
            VALUES ( %(first_name)s, %(last_name)s,\
            %(username)s, %(email)s, ('now'), %(password)s) RETURNING user_id;
            """
        curr.execute(query, user)
        user_id = curr.fetchone()[0]
        database.commit()
        curr.close()
        return int(user_id)
