from flask_wtf import Form
from flask import flash
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
                    ValidationError, SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo, \
                    IPAddress
from flask_login import login_user, logout_user, login_required, \
    current_user
from ..models import User, Role, Provider


from keystoneauth1 import identity
from keystoneauth1 import session
from neutronclient.v2_0 import client
from novaclient import client as client_nova

class AssignFloatingIP(Form):
    server = SelectField('Server', choices=int)

    
    def __init__(self, floatingip, *args, **kwargs):
        user = User.query.get_or_404(current_user.id)
        provider = Provider.query.get_or_404("1")
        auth = identity.Password(auth_url=provider.url,
                                 username=user.username,
                                 password=user.provider_password,
                                 project_name=user.username,
                                 project_domain_name='Default',
                                 user_domain_name='Default')
        sess = session.Session(auth=auth)
        nova = client_nova.Client('2', session=sess)
        servers = nova.servers.list()
        super(AssignFloatingIP, self).__init__(*args, **kwargs)
        self.server.choices = [(server.id, server.name)
                             for server in servers]
                             
        self.floatingip = floatingip
        
class UnAssignFloatingIP(Form):
    floatingip = StringField('Floating IP', validators=[Required(), Length(1, 128),
                                            IPAddress()])
    server = StringField('Server')
    submit = SubmitField()