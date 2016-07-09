# -*- coding: utf-8 -*-
import dateutil.parser

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_adminlte import AdminLTE

# main dash-stack app
dash = Flask(__name__)

# AdminLTE for flask; flask_adminlte
AdminLTE(dash)

# static configuration file
dash.config.from_object('config')

# db instance
db = SQLAlchemy(dash)
    
from dash import views, models