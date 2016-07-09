from flask import Flask, render_template
from flask_adminlte import AdminLTE
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

AdminLTE = AdminLTE()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
    dash = Flask(__name__)
    dash.config.from_object(config[config_name])
    config[config_name].init_app(dash)

    AdminLTE.init_app(dash)
    mail.init_app(dash)
    moment.init_app(dash)
    db.init_app(dash)
    
    
    # attach routes and custom error pages here
    
    from main import main as main_blueprint
    dash.register_blueprint(main_blueprint)
    
    return dash