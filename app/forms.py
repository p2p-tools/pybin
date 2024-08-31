from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FieldList, FormField
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError, DataRequired
import sqlalchemy as sa
from app import db
from app.models import User


class PasteForm(FlaskForm):
    filename = FieldList(StringField('Filename'), min_entries=1)
    value = FieldList(TextAreaField('Paste', validators=[DataRequired()]), min_entries=1)
    submit = SubmitField('create paste')
