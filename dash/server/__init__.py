from flask import Blueprint

server = Blueprint('server', __name__)

from . import views