from flask import Flask

import dateutil.parser

from flask_adminlte import AdminLTE


app = Flask(__name__)
AdminLTE(app)   


if __name__ == '__main__':
    create_app().run(debug=True)
    
from app import views, models