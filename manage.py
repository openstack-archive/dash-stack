from flask_script import Server, Shell, Manager

from dash import dash
from dash import models
from dash.models import db, User

def _make_context():
    return dict(dash=dash, db=db, models=models)

manager = Manager(dash)
manager.add_command("runserver", Server(host="0.0.0.0", port=8000))
manager.add_command("shell", Shell(make_context=_make_context))

if __name__ == "__main__":
    manager.run()