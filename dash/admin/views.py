import datetime, requests, json, string, random

from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from flask_principal import Identity, AnonymousIdentity, \
        identity_changed
    
from . import admin
from .. import db
from ..models import User, Role, Provider
from ..email import send_email
from ..decorators import requires_roles
from .forms import EditUserAdminForm, CreateUserAdminForm, CreateUserAdminForm, \
        DeleteUserAdminForm, CreateProviderAdminForm, EditProviderAdminForm, \
        DeleteProviderAdminForm, ValidateProviderAdminForm, \
        CreateUserProviderAdminForm 

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

@admin.route('/create-user-provider/<int:id>', methods=['GET', 'POST'])
@login_required
@requires_roles("admin")
def create_user_provider_admin(id):
    user = User.query.get_or_404(id)
    providers = Provider.query.all()
    form = CreateUserProviderAdminForm(user=user)
    if form.validate_on_submit():
        if len(user.provider_password) != 24:
            chars = string.letters + string.digits + string.punctuation
            user.provider_password = ''.join((random.choice(chars)) for x in range(24))
        db.session.add(user)
        # make openstack api connection for chosen provider
        provider = Provider.query.get_or_404(form.provider.data)
        auth = v3.Password(auth_url=provider.url,
                           username=provider.username,
                           password=provider.password,
                           project_id=provider.project_name,
                           user_domain_name='Default')
        sess = session.Session(auth=auth)
        keystone = client.Client(session=sess)
        # create project
        project = keystone.projects.create(user.username,
                                           'default',
                                           enabled=True)
        # creates user
        user = keystone.users.create(user.username,
                                    password=user.provider_password,
                                    email=user.email,
                                    enabled=True,
                                    default_project=user.username)
        role_search = keystone.roles.list(name=provider.default_role)
        role_id = role_search[0].id
        role = keystone.roles.grant(role_id,
                                    user=user.id,
                                    project=project.id)
        return render_template('admin/create_user_provider.html', user=user, form=form,
                                title="Create User on Provider", providers=providers,
                                project=project,role=role,
                                block_description = "create a user account on selected cloud provider")
    return render_template('admin/create_user_provider.html', user=user, form=form,
                            title="Create User on Provider", providers=providers,
                            block_description = "create a user account on selected cloud provider")
                            
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
        user.suspended = form.suspended.data
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
                            
@admin.route('/list-providers')
@login_required
@requires_roles("admin")
def list_providers():
    providers = Provider.query.all()
    return render_template('admin/list_providers.html', providers=providers,
                            title="List Providers",
                            block_description = "list, edit and delete providers")
                            
@admin.route('/create-provider', methods=['GET', 'POST'])
@login_required
@requires_roles("admin")
def create_provider_admin():
    form = CreateProviderAdminForm()
    if form.validate_on_submit():
        provider = Provider(provider=form.provider.data,
                    name=form.name.data,
                    project_name=form.project_name.data,
                    default_role=form.default_role.data,
                    username=form.username.data,
                    password=form.password.data,
                    api_version=form.api_version.data,
                    url=form.url.data,
                    created_at=datetime.datetime.now(),
                    enabled=form.enabled.data)
        db.session.add(provider)
        db.session.commit()
        flash('New provider created.')
        return redirect(url_for('.edit_provider_admin', id=provider.id))
    return render_template('admin/create_provider.html', form=form,
                            title="Create New Provider",
                            block_description = "add your new cloud provider")

@admin.route('/edit-provider/<int:id>', methods=['GET', 'POST'])
@login_required
@requires_roles("admin")                        
def edit_provider_admin(id):
    provider = Provider.query.get_or_404(id)
    form = EditProviderAdminForm(provider=provider)
    if form.validate_on_submit():
        provider.provider = form.provider.data
        provider.name = form.name.data
        provider.project_name = form.project_name.data
        provider.region = form.region.data
        provider.default_role=form.default_role.data
        provider.username = form.username.data
        provider.password = form.password.data
        provider.api_version = form.api_version.data
        provider.url = form.url.data
        provider.enabled = form.enabled.data
        db.session.add(provider)
        flash('The provider has been updated.')
        return redirect(url_for('.edit_provider_admin', id=provider.id))
    return render_template('admin/edit_provider.html', provider=provider, form=form,
                            title="Edit Provider",
                            block_description = "edit and update provider info")
                            
@admin.route('/delete-provider/<int:id>', methods=['GET', 'POST'])
@login_required
@requires_roles("admin")
def delete_provider_admin(id):
    provider = Provider.query.get_or_404(id)
    form = DeleteProviderAdminForm(provider=provider)
    if form.validate_on_submit():
        db.session.delete(provider)
        db.session.commit()
        flash('The provider has been deleted.')
        return redirect(url_for('.index'))
    return render_template('admin/delete_provider.html', provider=provider, form=form,
                            title="Delete Provider",
                            block_description = "delete provider confirmation")
                            
@admin.route('/validate-provider/<int:id>', methods=['GET', 'POST'])
@login_required
@requires_roles("admin")
def validate_provider_admin(id):
    provider = Provider.query.get_or_404(id)
    auth = v3.Password(auth_url=provider.url,
                       username=provider.username,
                       password=provider.password,
                       project_id=provider.project_name,
                       user_domain_name='Default')
    sess = session.Session(auth=auth)
    keystone = client.Client(session=sess)
    roles = keystone.roles.list(name='_member_')
    role_id = roles[0].id
    roles_type = type(roles)
    project = keystone.projects.list(name='admin')
    projects = 'projects'
    return render_template('admin/validate_provider.html', provider=provider,
                            title="Validate Provider", #projects=projects,
                            role_id=role_id,
                            keystone=keystone, roles=roles, project=project, roles_type=roles_type,
                            block_description = "validate provider")