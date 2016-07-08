# -*- coding: utf-8 -*-

from flask import render_template
from dash import dash

from .models import User

current_user = User()

@dash.route('/')
def index():
    return render_template('index.html',
                            title='Home',
                            current_user=current_user)

@dash.route('/login')
def login():
    return render_template('login.html',
                            title='Login',
                            current_user=current_user)

@dash.route('/lockscreen')
def lockscreen():
    return render_template('lockscreen.html', 
                            title='Lock',
                            current_user=current_user)