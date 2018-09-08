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

    def most_answered(self):
        """Obtains the question with the most answers"""
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("""SELECT question_id, COUNT(answer_id) FROM answers GROUP BY question_id ORDER BY COUNT(answer_id) DESC;""")
        data = curr.fetchone()
        return data

    def get_all(self):
        """This function returns a list of all the questions"""
        dbconn = self.db
        curr = dbconn.cursor()
        curr.execute("""SELECT * FROM questions;""")
        data = curr.fetchall()
        resp = []

        for i, items in enumerate(data):
            question_id, user_id, text, description, date = items
            question = dict(
                question_id=int(question_id),
                user_id=int(user_id),
                text=text,
                description=description,
                date_created=date
            )
            resp.append(question)
        return resp
