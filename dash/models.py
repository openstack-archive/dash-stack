# -*- coding: utf-8 -*-

import dateutil.parser
from dash import dash, db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    full_name = db.Column(db.String(128), index=True)
    avatar = "/static/img/user2-160x160.jpg"
    created_at = dateutil.parser.parse("November 12, 2012")
    
    def __refr__(self):
        return '<User %r>' % (self.nickname)