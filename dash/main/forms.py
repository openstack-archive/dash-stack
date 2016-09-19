from flask_wtf import Form
from flask import flash
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..models import User, Provider, Role


class SelectProvider(Form):
    provider = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')