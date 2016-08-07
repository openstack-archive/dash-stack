import datetime

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from flask_principal import Identity, AnonymousIdentity, \
     identity_changed
    
from . import admin
from .. import db
from ..models import User
from ..email import send_email
from ..decorators import requires_roles

@admin.route('/index')
@login_required
@requires_roles("admin")
def for_admins_only():
    return render_template('admin/index.html')