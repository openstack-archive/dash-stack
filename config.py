import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    DASH_MAIL_SUBJECT_PREFIX = '[dash-stack]'
    DASH_MAIL_SENDER = 'dash-stack Admin <kelepirci@dash-stack.org>'
    DASH_ADMIN = "ozkasgarli@gmail.com"
    
    @staticmethod
    def init_app(dash):
        pass
        
class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_TB_ENABLED = True
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        ('mysql+pymysql://root:Polo1043@localhost/dashDev')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'
    # Debug configuration
    FLASK_DEBUG = True
    SQLALCHEMY_ECHO = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        ('mysql://root:Polo1043@localhost/dashTest')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WTF_CSRF_ENABLED = False
        
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        ('mysql://root:Polo1043@localhost/dash')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'
        
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}