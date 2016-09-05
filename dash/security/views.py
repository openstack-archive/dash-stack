import datetime, requests, json, string, random

from keystoneauth1 import loading
from keystoneauth1 import session

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from flask_principal import Identity, AnonymousIdentity, \
        identity_changed
    
from . import security
from .. import db
from ..models import User, Role, Provider
from ..email import send_email
from ..decorators import requires_roles

@security.route('/', methods=['GET', 'POST'])
@login_required
@requires_roles("user","admin")
def index():
    return render_template('security/index.html')