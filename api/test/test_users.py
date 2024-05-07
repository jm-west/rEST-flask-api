import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from argon2 import PasswordHasher

class UserTestClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['test'])

        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()
        self.app = None
        self.client = None

    def test_user_signup(self):
        data = {
            "username": "testUser",
            "email": "test@user.com", 
            "password": "password123"
        }
        response = self.client.post('/auth/signup/',json=data)
        
        assert response.status_code == 201 