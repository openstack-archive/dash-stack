import dateutil.parser
from app import app


class User(object):
    """
    Example User object.  Based loosely off of Flask-Login's User model.
    """
    full_name = "Ferhat Ozkasgarli"
    avatar = "/static/img/user2-160x160.jpg"
    created_at = dateutil.parser.parse("November 12, 2012")