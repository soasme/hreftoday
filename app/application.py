# -*- coding: utf-8 -*-

from flask import Flask
from flask_nav.elements import Navbar, View
from flask_user import SQLAlchemyAdapter
from flask_appconfig import AppConfig
from flask_appconfig.env import from_envvars
from app.core import db, nav, bootstrap, user_manager, login_manager, mail, celery
from app.views import web
from app.models import User, UserInvitation
from app.consts import NAV_VIEWS
from app.utils.filters import FILTERS
from app.utils.jinja_tests import TESTS

def create_app(config_file=None):
    app = Flask('app')
    AppConfig(app, config_file)

    db.app = app
    db.init_app(app)

    bootstrap.app = app
    bootstrap.init_app(app)

    nav.app = app
    nav.register_element('top', Navbar('', *[View(*view) for view in NAV_VIEWS]))
    nav.init_app(app)

    login_manager.app = app
    login_manager.init_app(app)

    mail.app = app
    mail.init_app(app)

    #celery.app = app
    #celery.init_app(app)

    user_manager.init_app(
        app,
        db_adapter=SQLAlchemyAdapter(db, User, UserInvitationClass=UserInvitation),
        login_manager=login_manager
    )
    app.register_blueprint(web.bp)

    for jinja_filter in FILTERS:
        app.jinja_env.filters[jinja_filter] = FILTERS[jinja_filter]
    for jinja_test in TESTS:
        app.jinja_env.tests[jinja_test] = TESTS[jinja_test]
    return app
