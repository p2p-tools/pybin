from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FieldList, FormField
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError, DataRequired
import sqlalchemy as sa
from app import db
from app.models import User


class PasteForm(FlaskForm):
    filename = FieldList(StringField('Filename'), min_entries=1)
    value = FieldList(TextAreaField('Paste', validators=[DataRequired()]), min_entries=1)
    submit = SubmitField('Create paste')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
