import datetime

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
    
from . import admin
from .. import db
from ..models import User
from ..email import send_email

@admin.route('/')
@login_required
def for_admins_only():
    return render_template('admin/index.html')