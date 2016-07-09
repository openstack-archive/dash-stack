from flask import current_app

app = Flask(__name__)
with app.app_context():
    # within this block, current_app points to app.
    print current_app.name