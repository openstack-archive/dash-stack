# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = 
    remember_me = BooleanField('remember_me', default=False)