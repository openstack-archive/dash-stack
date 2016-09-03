import datetime, requests, json, string, random

from keystoneauth1 import loading
from keystoneauth1 import session
from novaclient import client

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from flask_principal import Identity, AnonymousIdentity, \
        identity_changed
    
from . import server
from .. import db
from ..models import User, Role, Provider
from ..email import send_email
from ..decorators import requires_roles

@server.route('/', methods=['GET', 'POST'])
@login_required
@requires_roles("user","admin")
def index():
    return render_template('server/index.html')
    
@server.route('/list-servers', methods=['GET', 'POST'])
@login_required
@requires_roles("user","admin")
def list_servers():
    user = User.query.get_or_404(current_user.id)
    provider = Provider.query.get_or_404("1")
    loader = loading.get_plugin_loader('password')
    auth = loader.load_from_options(auth_url=provider.url,
                                    username=user.username,
                                    password=user.provider_password,
                                    project_name=user.username,
                                    project_domain_name='Default',
                                    user_domain_name='Default')
    sess = session.Session(auth=auth)
    nova = client.Client('2', session=sess)
    servers = nova.servers.list()
    return render_template('server/list_servers.html',
                           title="List Servers",
                           block_description = "list your servers",
                           user=user, provider=provider,nova=nova,
                           servers=servers)