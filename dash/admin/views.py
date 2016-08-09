import datetime

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from flask_principal import Identity, AnonymousIdentity, \
     identity_changed
    
from . import admin
from .. import db
from ..models import User, Role
from ..email import send_email
from ..decorators import requires_roles
from .forms import EditProfileAdminForm

@admin.route('/')
@login_required
@requires_roles("admin")
def index():
    return render_template('admin/index.html')
    
@admin.route('/list-users')
@login_required
@requires_roles("admin")
def list_users():
    users = User.query.all()
    return render_template('admin/list_users.html', users=users,
                            title="List Users",
                            block_description = "list, edit and delete users")
    
@admin.route('/edit-user/<int:id>', methods=['GET', 'POST'])
@login_required
@requires_roles("admin")
def edit_user_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.full_name = form.full_name.data
        user.role_id = Role.query.get(form.role.data)
        user.confirmed = form.confirmed.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    return render_template('admin/edit_user.html', user=user, form=form,
                            title="Edit User",
                            block_description = "edit and update user info")