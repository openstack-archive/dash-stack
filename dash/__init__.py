# -*- coding: utf-8 -*-

from flask import Flask

import dateutil.parser

from flask_adminlte import AdminLTE


dash = Flask(__name__)
AdminLTE(dash)

    
from dash import views, models