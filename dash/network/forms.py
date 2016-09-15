from flask_wtf import Form
from flask import flash
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
                    ValidationError, SelectField 
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, \
                    IPAddress
from ..models import User, Role, Provider

from flask_login import login_user, logout_user, login_required, \
    current_user

from keystoneauth1 import identity
from keystoneauth1 import session
from neutronclient.v2_0 import client
from novaclient import client as client_nova

class AssignFloatingIP(Form):
    floatingip = StringField('Floating IP', validators=[Required(), Length(1, 128),
                                            IPAddress()])
    server = SelectField('Server', choices = [])