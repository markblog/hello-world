import os
import logging
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '0x1092-3dfe834-324few23-342dlej'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    DATABASE_QUERY_TIMEOUT = 0.01
    SQLALCHEMY_ECHO = True
    LOGGING_FORMAT = """[%(levelname)s] - %(asctime)s : %(message)s
%(module)s [%(pathname)s:%(lineno)d]
    """
    LOGGING_LOCATION = 'log/debug.log'
    LOGGING_LEVEL = logging.DEBUG
    
    DATA_FOLDER = ''
    EXCLUDE_RULES = ['/api/v2/messages/count']

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'postgresql://postgres:gxtagging@localhost/aa_dev'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'postgresql://postgres:123456@localhost/aa_test'


class ProductionConfig(Config):
    LOGGING_LOCATION = 'log/errors.log'
    LOGGING_LEVEL = logging.ERROR
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:123456@localhost/aa'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


