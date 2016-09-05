import datetime, requests, json, string, random
import humanize as humanize

from keystoneauth1 import loading
from keystoneauth1 import session
import glanceclient.v2.client as glclient

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from flask_principal import Identity, AnonymousIdentity, \
        identity_changed
    
from . import image
from .. import db
from ..models import User, Role, Provider
from ..email import send_email
from ..decorators import requires_roles

@image.route('/', methods=['GET', 'POST'])
@login_required
@requires_roles("user","admin")
def index():
    return render_template('image/index.html')
    
@image.route('/list-images', methods=['GET', 'POST'])
@login_required
@requires_roles("user","admin")
def list_images():
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
    glance = glclient.Client('2', session=sess)
    images = glance.images.list()
    return render_template('image/list_images.html',humanize=humanize,
                           title="List Imags",
                           block_description = "list images and applications",
                           user=user, provider=provider,glance=glance,
                           images=images)