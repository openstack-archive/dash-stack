import unittest
from dash.models import User

class UserModelTestCase(unittest.TestCase):
    def test_password(self):
        u = User(password = 'cat')
        self.assertTrue(u.password_hash is not None)
        
    def no_password_getter(self):
        u = User(password = 'cat')
        with self.assertRaises(AttributeError):
            u.password
            
    def test_password_verification(self):
        u = User(password = 'cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))
        
    def test_password_salt_are_random(self):
        u = User(password = 'cat')
        u2 = User(password = 'cat')
        self.assertTrue(u.password_hash != u2.password_hash)
        
if __name__ == '__main__':
    unittest.main()