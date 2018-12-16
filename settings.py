from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os

db = SQLAlchemy()
bootstrap = Bootstrap()

DEBUG = True

WTF_CSRF_ENABLED = False
TEMPLATES_AUTO_RELOAD = True

# WTF_CSRF_ENABLED = False
SECRET_KEY = os.urandom(24)

basedir = os.path.abspath('.')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir + '/', 'data.sqlite')

PER_PAGE = 10
