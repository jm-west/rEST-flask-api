from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .orders.views import orders_namespace
from .auth.views import auth_namespace
from .config.config import config_dict
from .utils import db
from .models.orders import Order
from .models.users import User


def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config) 
    api = Api(app)
    api.add_namespace(orders_namespace)
    api.add_namespace(auth_namespace,path='/auth')
    db.init_app(app)
    jwt = JWTManager(app) 
    migrate = Migrate(app, db)
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db, 
            'Orders': Order,
            'Users': User
        }
    return app
