import dateutil.parser

from flask import render_template, redirect, request, url_for, flash, \
    current_app, session
from flask_login import login_user, logout_user, login_required, \
    current_user
from flask_principal import Identity, AnonymousIdentity, \
        identity_changed


from .. import db
from ..models import User, Provider, Role
from ..email import send_email
from . import main
from ..decorators import requires_roles
from .forms import SelectProvider

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('main.index')

@main.route('/', methods=['GET', 'POST'])
@login_required
@requires_roles("user","reseller","admin")
def index():
    return render_template('index.html')
    
@main.route('/reseller')
@login_required
@requires_roles("user","reseller","admin")
def for_resellers_only():
    return "For resellers only! We mean it..."
    

@main.route('/select-provider/<int:id>')
@login_required
@requires_roles("user","reseller","admin")
def select_provider(id):
    provider = Provider.query.filter_by(id=id).first()
    if provider:
        session['selected_provider'] = id
    return redirect(redirect_url())
