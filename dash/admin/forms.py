from flask_wtf import Form
from flask import flash
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
                    ValidationError, SelectField 
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..models import User, Role

class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 128),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    full_name = StringField('Full name', validators=[Required(), Length(1, 255)])
    role_id = SelectField('Role', coerce=int)
    confirmed = BooleanField('Confirmed')
    
    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role_id.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user
        
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
            
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')