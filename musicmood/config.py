import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '4694c8c0-f2e3-4916-b65e-5ed070d14b3d'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///music.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    ENV = 'development'

config = Config()
