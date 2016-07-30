import datetime
import unittest
import tempfile
import dash

from flask import current_app
from flask_testing import TestCase
from flask_login import login_user, logout_user, login_required, \
    current_user

from dash import create_app, db
from dash.models import User

class ViewFunctionsTestCase(unittest.TestCase):
    def setUp(self):
        self.dash = create_app('testing')
        self.app_context = self.dash.app_context()
        self.app_context.push()
        self.app_test_client = self.dash.test_client()
        db.create_all()  
        # create user for testing
        u = User(email="test@dash-stack.org",
                    username="test",
                    full_name="Dash Stack",
                    password="test",
                    avatar="/static/img/user2-160x160.jpg",
                    created_at=datetime.datetime.now())
        db.session.add(u)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    # test user registration
    def user_register(self, email, username, full_name, password, password2, terms):
        return self.app_test_client.post('/auth/register',
            data=dict(
            email=email,
            username=username,
            full_name=full_name,
            password=password,
            password2=password2,
            terms=terms), follow_redirects=True)
            
    def test_user_registration(self):
        rv = self.user_register('test2@dash-stack.org',
                                'test2',
                                'Dash Stack the Second',
                                'test2',
                                'test2',
                                True)
        assert 'You can now login.' in rv.data
        
    # user login function
    def login(self, email, password):
        return self.app_test_client.post('/auth/login',
            data=dict(
            email=email,
            password=password), follow_redirects=True)
    
    # user logout function
    def logout(self):
        return self.app_test_client.get('/auth/logout', follow_redirects=True)
        
    # test user login and logout
    def test_login_logout(self):
        rv = self.login('test@dash-stack.org', 'test')
        assert 'Dash Stack - Web Developer' in rv.data
        rv = self.logout()
        assert 'You have been logged out.' in rv.data
        rv = self.login('testx@dash-stack.org', 'test')
        assert 'Invalid username or password.' in rv.data
        rv = self.login('test@dash-stack.org', 'testx')
        assert 'Invalid username or password.' in rv.data
        
        
if __name__ == '__main__':
    unittest.main()