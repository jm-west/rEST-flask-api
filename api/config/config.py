import os
from decouple import config
from datetime import timedelta 

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRECT_KEY = config('SECRECT_KEY','secret') 
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES =timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = config('DEBUG',cast=bool)
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

class TestConfig(Config):
    pass

class ProdConfig(Config):
    pass



config_dict = {
    "dev": DevConfig, 
    "test": TestConfig,
    "prod": ProdConfig
 }
