from flask_wtf import Form
from flask import flash
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..models import User

class ChangePasswordForm(Form):
    old_password = PasswordField('Password', validators=[Required()])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    type = StringField()
    
class UpdateProfileForm(Form):
    full_name = StringField('Full name', validators=[Required(), Length(1, 255)])
    type = StringField()
    
    def validate_full_name(self, field):
        if User.query.filter_by(full_name=field.data).first():
            raise ValidationError('You have not changed your full name.')
            
class ChangeUserNameForm(Form):
    username = StringField('Username', validators=[
                Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    type = StringField()
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')
            
class ChangeEmailForm(Form):
    email = StringField('New Email', validators=[Required(), Length(1, 128),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    type = StringField()
                                             
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')