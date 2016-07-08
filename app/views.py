from flask import render_template
from app import app

from .models import User

current_user = User()

@app.route('/')
def index():
    return render_template('index.html', current_user=current_user)

@app.route('/login')
def login():
    return render_template('login.html', current_user=current_user)

@app.route('/lockscreen')
def lockscreen():
    return render_template('lockscreen.html', current_user=current_user)