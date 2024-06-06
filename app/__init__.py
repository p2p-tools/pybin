from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_login import LoginManager

from config import Config

app = Flask(__name__)
login = LoginManager(app)
app.config.from_object(Config)

CONVENTION = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=CONVENTION)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

from app import routes, models


@login.user_loader
def load_user(id):
    return db.session.get(models.User, int(id))
