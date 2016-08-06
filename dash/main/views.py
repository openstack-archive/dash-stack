import dateutil.parser

from flask import render_template, session, redirect, url_for, current_app

from flask_login import login_required


from .. import db
from ..models import User, Permission
from ..email import send_email
from . import main
from .forms import NameForm
from ..decorators import admin_required, permission_required


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')
    
@main.route('/lockscreen')
def lockscreen():
    current_user = User()
    return render_template('lockscreen.html', current_user=current_user)
    
@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators only!"
    
@main.route('/reseller')
@login_required
@permission_required(Permission.LIST_USER)
def for_resellers_only():
    return "For resellers only! We mean it..."