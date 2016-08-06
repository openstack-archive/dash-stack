import dateutil.parser
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask import current_app

from flask_login import UserMixin, AnonymousUserMixin

from . import db
from . import login_manager

# user roles
class Permission:
    ## user permissions
    # instance management
    LAUNCH_INSTANCE = 0x1A
    REMOVE_INSTANCE = 0x2A
    MANAGE_INSTANCE = 0x3A
    LIST_INSTANCE = 0x4A
    
    ## reseller permissions
    # Users Management
    CREATE_USER = 0x1B
    MANAGE_USER = 0x2B
    DELETE_USER = 0x3B
    LIST_USER = 0x4B
    SUSPEND_USER = 0x5B
    UNSUSPEND_USER = 0x6B
    
    # Tenant Management
    CREATE_TENANT = 0x7B
    MANAGE_TENANT = 0x8B
    DELETE_TENANT = 0x9B
    LIST_TENANT = 0xB1
    SUSPEND_TENANT = 0xB2
    UNSUSPEND_TENANT = 0xB3
    MODIFY_TENANT_QUOTA = 0xB4
    
    # administrator permissions
    ADMINISTER = 0xff

class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    # creates roles and permissions in db
    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.LAUNCH_INSTANCE |
                     Permission.REMOVE_INSTANCE |
                     Permission.MANAGE_INSTANCE |
                     Permission.LIST_INSTANCE, True),
            'Reseller': (Permission.CREATE_USER |
                          Permission.MANAGE_USER |
                          Permission.DELETE_USER |
                          Permission.LIST_USER |
                          Permission.SUSPEND_USER |
                          Permission.UNSUSPEND_USER |
                          # tenant management
                          Permission.CREATE_TENANT |
                          Permission.MANAGE_TENANT |
                          Permission.DELETE_TENANT |
                          Permission.LIST_TENANT |
                          Permission.SUSPEND_TENANT |
                          Permission.UNSUSPEND_TENANT |
                          Permission.MODIFY_TENANT_QUOTA, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()
        
    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    full_name = db.Column(db.String(255), index=True)
    avatar = db.Column(db.String(255), index=True)
    created_at = db.Column(db.DateTime)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)
                
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # generates confirmation token for user email confirmation
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})
    
    # confirms user email by id
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True
    
    # generates token for password reset
    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})
        
    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True
        
    # generates token for email change
    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})
    
    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True
        
    # Role assignment
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['DASH_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
                
    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions
        
        def is_administrator(self):
            return self.can(Permission.ADMINISTER)
                
    def __repr__(self):
        return '<User %r>' % self.username

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    
    def is_administrator():
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))