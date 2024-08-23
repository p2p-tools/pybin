import os

from dotenv import dotenv_values

config = dotenv_values(".env")
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = config.get('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    ENCRYPTION_KEY = config.get("ENC_KEY", "_sOncN8Fv-Rri6otHmLqOSmLw9rTXPOv-w_nJji03xI=")
