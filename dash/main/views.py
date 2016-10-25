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
    user = User.query.filter_by(id=current_user.id).first()
    if provider:
        user.selected_provider_id = id
        db.session.add(user)
        flash('%s has been selected.' % provider.name)
    return redirect(redirect_url())
    
@main.route('/all-providers')
@login_required
@requires_roles("user","reseller","admin")
def all_providers():
    providers = Provider.query.all()
    return render_template('all_providers.html',
                            title="All Providers",
                            block_description = "list of all providers",
                            providers=providers)
