"""
This module defines the base model and associated functions
"""
from datetime import datetime, timedelta
import jwt
import os
from .... import create_app

from ....database import init_db


class BaseModel(object):
    """
    This class encapsulates the functions of the base model
    that will be shared across all other models
    """

    def __init__(self):
        """initialize the database"""
        self.db = init_db()

    def get_items_by_id(self, item, item_id):
        """
        return a list of all the items with the id given
        used by question and answer models
        """
        table_name = "%ss" % (self._type().lower()[:-5])
        database = self.db
        item_name = table_name[:-1]
        curr = database.cursor()
        curr.execute("""SELECT %s_id, user_id, text, date_created\
                     FROM %s WHERE %s_id = %d;""" % (item_name, table_name,
                                                     item,
                                                     item_id)
                     )
        data = curr.fetchall()
        curr.close()
        # return a list of dictionaries
        resp = []
        for i, items in enumerate(data):
            item_id, user_id, text, date_created = items
            username = self.get_username_by_id(int(user_id))
            item_dict = {
                "%s_id" % (item_name): int(item_id),
                "username": username,
                "text": text,
                "date_created": date_created
            }
            resp.append(item_dict)
        return resp

    def get_item_by_id(self, item_id):
        """returns an entire record by searching for the id number"""
        try:
            dbconn = self.db
            curr = dbconn.cursor()
            table_name = "%ss" % (self._type().lower()[:-5])
            item_name = table_name[:-1]
            curr.execute(
                """SELECT * FROM %s WHERE %s_id = %d;""" % (table_name,
                                                            item_name,
                                                            int(item_id)))
            data = curr.fetchone()
            curr.close()
            return data
        except Exception as e:
            return "Not Found"

    def delete_item(self, item_id, foreign_key):
        """This function takes an id and removes the corresponding item from the database"""
        try:
            table_name = "%ss" % (self._type().lower()[:-5])
            item_name = table_name[:-1]
            dbconn = self.db
            curr = dbconn.cursor()
            fk_query = "DELETE FROM %s WHERE %s_id = %d;" % (foreign_key,
                                                             item_name,
                                                             int(item_id))
            curr.execute(fk_query)
            dbconn.commit()
            query = "DELETE FROM %s WHERE %s_id = %d;" % (table_name,
                                                          item_name,
                                                          int(item_id))
            curr.execute(query)
            curr.close()
            dbconn.commit()
        except Exception as e:
            return "Not Found"
        pass

    def update_item(self, field, data, item_id):
        """update the field of an item given the item_id"""
        try:
            if not isinstance(data, str):
                raise ValueError
            table_name = "%ss" % (self._type().lower()[:-5])
            item_name = table_name[:-1]
            dbconn = self.db
            curr = dbconn.cursor()
            curr.execute("UPDATE %s SET %s = '%s' \
                         WHERE %s_id = %d RETURNING text;" % (table_name,
                                                              field,
                                                              data,
                                                              item_name,
                                                              item_id))
            updated_field = curr.fetchone()
            dbconn.commit()
            return updated_field
        except ValueError:
            return "Data must be a string"
        except Exception as e:
            return e

    def get_username_by_id(self, user_id):
        """returns a username given the id"""
        try:
            dbconn = self.db
            curr = dbconn.cursor()
            curr.execute(
                """SELECT username FROM users WHERE user_id = %d;""" % (user_id))
            data = curr.fetchone()
            curr.close()
            return data[0]
        except Exception:
            return "Not Found"

    @staticmethod
    def encode_auth_token(user_id):
        """Function to generate Auth token
        """
        APP = create_app()
        # import pdb;pdb.set_trace()
        try:
            payload = {
                "exp": datetime.utcnow() + timedelta(days=1),
                "iat": datetime.utcnow(),
                "sub": user_id
            }
            token = jwt.encode(
                payload,
                APP.config.get('SECRET_KEY'),
                algorithm="HS256"
            )
            resp = token
        except Exception as e:
            resp = e

        return resp

    def blacklisted(self, token):
        dbconn = self.db
        curr = dbconn.cursor()
        query = """
                SELECT * FROM blacklist WHERE tokens = %s;
                """
        curr.execute(query, [token])
        if curr.fetchone():
            return True
        return False

    def decode_auth_token(self, auth_token):
        """This function takes in an auth 
        token and decodes it
        """
        if self.blacklisted(auth_token):
            return "Token has been blacklisted"
        APP = create_app()
        secret = APP.config.get("SECRET_KEY")
        try:
            payload = jwt.decode(auth_token, secret)
            return payload['sub']  # user id
        except jwt.ExpiredSignatureError:
            return "The token has expired"
        except jwt.InvalidTokenError:
            return "The token is invalid"

    def check_text_exists(self, text):
        """Checks if the question or answer passed by the user exists"""
        table_name = "%ss" % (self._type().lower()[:-5])
        item_name = item_name = table_name[:-1]
        conn = self.db
        curr = conn.cursor()
        query = """
                SELECT %s_id FROM %s WHERE text = '%s';
                """ % (item_name, table_name, text)
        curr.execute(query)
        item = curr.fetchone()
        if not item:
            # no question exists with that username
            return "Not Found"
        return int(item[0])

    def _type(self):
        """returns the name of the inheriting class"""
        return self.__class__.__name__

    def close_db(self):
        """This function closes the database"""
        self.db.close()
        pass
