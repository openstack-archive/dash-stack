import dateutil.parser

from flask import render_template, session, redirect, url_for, current_app

from flask_login import login_required


from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')
    
@main.route('/lockscreen')
def lockscreen():
    current_user = User()
    return render_template('lockscreen.html', current_user=current_user)
    
@main.route('/reseller')
@login_required
def for_resellers_only():
    return "For resellers only! We mean it..."