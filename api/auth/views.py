from flask_restx import Namespace,Resource,fields
from flask import request
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required,get_jwt_identity
from ..models.users import User
from werkzeug.security import generate_password_hash,check_password_hash
from argon2 import PasswordHasher
from http import HTTPStatus
from werkzeug.exceptions import Conflict,Unauthorized


ph = PasswordHasher()

auth_namespace =  Namespace('auth', description='Authentication operations')

signUp_model = auth_namespace.model("SignUp",{
    "id": fields.Integer,
    "username": fields.String(required=True,description="A Username"),
    "email": fields.String(required=True,description="An Email"),
    "password": fields.String(required=True,description="A Password"),
    }
)

user_model = auth_namespace.model("User",{
    "id": fields.Integer,
    "username": fields.String(required=True,description="A Username"),
    "email": fields.String(required=True,description="An Email"),
    "password": fields.String(required=True,description="A Password"),
    "is_active": fields.Boolean(description="Is the user active?"),
    "is_staff": fields.Boolean(description="Is the user staff?"),
    }
)

login_model = auth_namespace.model("login",{
    "email": fields.String(required=True,description="An Email"),
    "password": fields.String(required=True,description="A Password"),
    }
)


@auth_namespace.route('/signup')
class SignUp(Resource):
    @auth_namespace.expect(signUp_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """
        Creates a new user
        """
        data = request.get_json()

        try:
            new_user = User(
                username = data.get('username'),
                email = data.get('email'),
                passwordHash = ph.hash(data.get('password'))
            )
            new_user.save()

            return new_user,HTTPStatus.CREATED
        except Exception as e:
            raise Conflict(f"User with {data.get('email')} already exists")

@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
        Generates a JWT
        """
        data = request.get_json()
        email = data.get('email')
        user = User.query.filter_by(email=email).first() 
        if (user is not None) and ph.verify(user.passwordHash,data.get('password')):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)
            response ={
                "access_token": access_token,
                "refresh_token": refresh_token 
            }
            return response,HTTPStatus.OK
        raise Unauthorized("Invalid Credentials")

@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
        Refreshes a JWT
        """
        username = get_jwt_identity()
        accesse_token = create_access_token(identity=username)
        
        return {"accesse_token":accesse_token},HTTPStatus.OK
