import os

from dotenv import dotenv_values

config = dotenv_values(".env")
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = config.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
