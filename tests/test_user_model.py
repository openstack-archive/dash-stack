import datetime
import unittest

from dash.models import User
from dash import db, create_app

from flask import current_app

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.dash = create_app('testing')
        self.app_context = self.dash.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_password_setter(self):
        u = User(password = 'cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password = 'cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password = 'cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))
        
    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)
        
    def test_create_user_and_check(self):
        u = User(email="test@dash-stack.org",
                    username="test",
                    full_name="Dash Stack",
                    password="test",
                    avatar="/static/img/user2-160x160.jpg",
                    created_at=datetime.datetime.now())
        db.session.add(u)
        u = User.query.filter_by(email="test@dash-stack.org").first()
        self.assertTrue(u.email == "test@dash-stack.org")
        
if __name__ == '__main__':
    unittest.main()