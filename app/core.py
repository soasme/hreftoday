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

db = SQLAlchemy()
nav = Nav()
bootstrap = Bootstrap()
login_manager = LoginManager()
user_manager = UserManager()
mail = Mail()
celery = Celery()
sentry = Sentry()
admin = Admin(template_mode='bootstrap3')
