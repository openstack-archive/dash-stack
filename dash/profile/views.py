import datetime
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import profile
from .. import db
from ..models import User
from ..email import send_email
from .forms import ChangePasswordForm, UpdateProfileForm, ChangeUserNameForm, \
    ChangeEmailForm


@profile.route('/', methods=['GET', 'POST'])
@login_required
def index():
    formChangePassword = ChangePasswordForm()
    formChangeUserName = ChangeUserNameForm()
    formUpdateProfile = UpdateProfileForm()
    formChangeEmail = ChangeEmailForm()
    
    if formChangePassword.type.data == 'formChangePassword':
        if formChangePassword.validate_on_submit():
            if current_user.verify_password(formChangePassword.old_password.data):
                current_user.password = formChangePassword.password.data
                db.session.add(current_user)
                flash('You password has been changed.')
                send_email(current_user.email, 'You Password has Changed', 
                   'profile/email/password_changed', user=current_user)
                return redirect(url_for('profile.index'))
            else:
                flash('Invalid password.')
            return redirect(url_for('profile.index'))
    if formChangeUserName.type.data == 'formChangeUserName':
        if formChangeUserName.validate_on_submit():
            current_user.username = formChangeUserName.username.data
            db.session.add(current_user)
            flash('formChangeUserName')
            return redirect(url_for('profile.index'))
    if formUpdateProfile.type.data == 'formUpdateProfile':
        if formUpdateProfile.validate_on_submit():
            current_user.full_name = formUpdateProfile.full_name.data
            db.session.add(current_user)
            flash('formUpdateProfile')
            return redirect(url_for('profile.index'))
    if formChangeEmail.type.data == 'formChangeEmail':
        if formChangeEmail.validate_on_submit():
            if current_user.verify_password(formChangeEmail.password.data):
                new_email = formChangeEmail.email.data
                token = current_user.generate_email_change_token(new_email)
                send_email(new_email, 'Confirm your email address',
                       'profile/email/change_email',
                       user=current_user, token=token)
                flash('An email with instructions to confirm your new email '
                      'address has been sent to you.')
                return redirect(url_for('profile.index'))
            else:
                flash('Invalid email address or password.')
    return render_template('profile/index.html',
                            formChangePassword=formChangePassword,
                            formChangeUserName=formChangeUserName,
                            formUpdateProfile=formUpdateProfile,
                            formChangeEmail=formChangeEmail)
                            
@profile.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('profile.index'))
