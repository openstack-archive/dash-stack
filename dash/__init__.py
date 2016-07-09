# -*- coding: utf-8 -*-
import dateutil.parser

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_adminlte import AdminLTE
from flask_login import LoginManager

# main dash-stack app
dash = Flask(__name__)

# AdminLTE for flask; flask_adminlte
AdminLTE(dash)

# static configuration file
dash.config.from_object('config')

# db instance
db = SQLAlchemy(dash)

# login manager; flask_login
login_manager = LoginManager()
login_manager.session_protetion = 'strong'
login_manager.login_view = 'login'
    
from dash import views, models