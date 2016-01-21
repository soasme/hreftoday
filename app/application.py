# -*- coding: utf-8 -*-

from flask import Flask
from flask_nav.elements import Navbar, View
from flask_user import SQLAlchemyAdapter
from flask_appconfig import AppConfig
from flask_appconfig.env import from_envvars
from app.core import db, nav, bootstrap, user_manager, login_manager, mail
from app.views import web
from app.models import User

def create_app(config_file=None):
    app = Flask('app')
    AppConfig(app, config_file)

    db.app = app
    db.init_app(app)
    db.create_all()

    bootstrap.app = app
    bootstrap.init_app(app)

    nav.app = app
    nav.register_element('top', Navbar('', View('Home', 'web.index')))
    nav.init_app(app)

    login_manager.app = app
    login_manager.init_app(app)

    mail.app = app
    mail.init_app(app)

    user_manager.init_app(app, db_adapter=SQLAlchemyAdapter(db, User), login_manager=login_manager)
    app.register_blueprint(web.bp)
    return app
