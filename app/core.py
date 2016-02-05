# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask_nav import Nav
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_user import UserManager
from flask_mail import Mail
from flask_celery import Celery
from raven.contrib.flask import Sentry
from flask_admin import Admin
from flask_cache import Cache
from flask_oauthlib.provider import OAuth2Provider
from flask_gravatar import Gravatar
from flask_restless import APIManager

db = SQLAlchemy()
nav = Nav()
bootstrap = Bootstrap()
login_manager = LoginManager()
user_manager = UserManager()
mail = Mail()
celery = Celery()
sentry = Sentry()
admin = Admin(template_mode='bootstrap3')
cache = Cache()
oauth = OAuth2Provider()
gravatar = Gravatar()
api_manager = APIManager(flask_sqlalchemy_db=db)
