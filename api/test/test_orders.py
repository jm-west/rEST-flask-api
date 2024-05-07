import unittest
from .. import create_app
from ..config.config import config_dict
from ..models.orders import Order
from ..utils import db
from flask_jwt_extended import create_access_token 

class OrdersTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['test'])
        self.app_context  = self.app.test_client()  
        self.app_context.push()
        self.client = self.app.test_client()

        db.create_all( )

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()
        self.app = None
        self.client = None


    def test_get_all_orders(self):
        token = create_access_token(identity="testUser")
        headers = {"Authoritzation" : f"Bearer {token}"}
        response = self.client.get('/orders/order',headers=headers)
        assert response.status_code == 200
        assert response.data == []
