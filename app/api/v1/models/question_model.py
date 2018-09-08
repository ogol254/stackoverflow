"""
This module defines the questions model and associated functions
"""
from datetime import datetime, timedelta

from flask import current_app

# local imports
from .... import create_app
from ....database import init_db
from .base_model import BaseModel


class QuestionModel(BaseModel):
    """This class encapsulates the functions of the question model"""

    def __init__(self, user_id=0, text="text", description="desc"):
        """initialize the question model"""
        self.user_id = user_id
        self.text = text
        self.description = description
        self.date_created = datetime.now()
        self.db = init_db()

    def save_question(self):
        """Add question details to the database"""
        question = {
            "user_id": self.user_id,
            "text": self.text,
            "description": self.description
        }
        database = self.db
        curr = database.cursor()
        query = """INSERT INTO questions (user_id, text, description, date_created) VALUES (%(user_id)s, %(text)s,\
                %(description)s, ('now')) RETURNING question_id;"""
        curr.execute(query, question)
        question_id = curr.fetchone()[0]
        database.commit()
        curr.close()
        return int(question_id)
