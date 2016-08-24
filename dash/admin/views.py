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
from .forms import EditUserAdminForm, CreateUserAdminForm, CreateUserAdminForm, \
        DeleteUserAdminForm

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

@admin.route('/create-user', methods=['GET', 'POST'])
@login_required
@requires_roles("admin")
def create_user_admin():
    form = CreateUserAdminForm()
    if form.validate_on_submit():
        r = Role.query.filter_by(default=True).first()
        user = User(email=form.email.data,
                    username=form.username.data,
                    full_name=form.full_name.data,
                    password=form.password.data,
                    avatar="/static/img/user2-160x160.jpg",
                    created_at=datetime.datetime.now(),
                    role_id=r.id,
                    confirmed=form.confirmed.data)
        db.session.add(user)
        db.session.commit()
        flash('New user created.')
        return redirect(url_for('.edit_user_admin', id=user.id))
    return render_template('admin/create_user.html', form=form,
                            title="Create New User",
                            block_description = "fill all the fields to create new user")
                            
@admin.route('/edit-user/<int:id>', methods=['GET', 'POST'])
@login_required
@requires_roles("admin")
def edit_user_admin(id):
    user = User.query.get_or_404(id)
    roles = Role.query.filter_by().all()
    form = EditUserAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.full_name = form.full_name.data
        user.role = Role.query.get(form.role.data)
        user.confirmed = form.confirmed.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.edit_user_admin', id=user.id))
    return render_template('admin/edit_user.html', user=user, form=form,
                            roles=roles,
                            title="Edit User",
                            block_description = "edit and update user info")
                            
@admin.route('/delete-user/<int:id>', methods=['GET', 'POST'])
@login_required
@requires_roles("admin")
def delete_user_admin(id):
    user = User.query.get_or_404(id)
    form = DeleteUserAdminForm(user=user)
    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        flash('The user has been deleted.')
        return redirect(url_for('.index'))
    return render_template('admin/delete_user.html', user=user, form=form,
                            title="Delete User",
                            block_description = "delete user confirmation")