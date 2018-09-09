import os
import unittest

# class for handling a set of commands
from flask_script import Manager
import nose
from app import db, create_app, init_test_db

# initialize the app with all its configurations
app = create_app(config_name=os.getenv('APP_SETTINGS'))

manager = Manager(app)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    nose.run()


@manager.command
def createall():
    "Create database tables"
    init_test_db()


@manager.shell
def make_shell_context():
    "Format response"
    return dict(app=current_app, db=db)


if __name__ == '__main__':
    manager.run()
