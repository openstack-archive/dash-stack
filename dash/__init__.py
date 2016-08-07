from flask import Flask, render_template

from flask_adminlte import AdminLTE
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension

from config import config


AdminLTE = AdminLTE()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
toolbar = DebugToolbarExtension()

# initialize flask_login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

# user loader call back function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_name):
    dash = Flask(__name__)
    dash.config.from_object(config[config_name])
    config[config_name].init_app(dash)
    
    
    AdminLTE.init_app(dash)
    mail.init_app(dash)
    moment.init_app(dash)
    db.init_app(dash)
    login_manager.init_app(dash)
    toolbar.init_app(dash)
    
    
    # attach routes and custom error pages here
    
    # main application
    from main import main as main_blueprint
    dash.register_blueprint(main_blueprint)
    
    # auth application
    from .auth import auth as auth_blueprint
    dash.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    # user profile application
    from .profile import profile as profile_blueprint
    dash.register_blueprint(profile_blueprint, url_prefix='/profile')
    
    # admin application
    from .admin import admin as admin_blueprint
    dash.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    return dash