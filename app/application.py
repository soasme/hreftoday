# -*- coding: utf-8 -*-

import logging
from flask import Flask
from flask_nav.elements import Navbar, View
from flask_user import SQLAlchemyAdapter
from flask_appconfig import AppConfig
from flask_appconfig.env import from_envvars
from app.core import sentry
from app.core import db, nav, bootstrap, user_manager, login_manager, mail, celery, admin
from app.views import web
from app.views.admin import AdAdminView, LinkAdminView, IssueAdminView
from app.models import User, UserInvitation, Ad, Link, Issue
from app.consts import NAV_VIEWS
from app.utils.filters import FILTERS
from app.utils.jinja_tests import TESTS

def create_app(config_file=None):
    app = Flask('app')

    AppConfig(app, config_file)

    stream = logging.StreamHandler()
    stream.setFormatter(logging.Formatter(
        '%(name)s %(levelname)s %(asctime)s "%(message)s"'
    ))
    admin_logger = logging.getLogger('app.admin')
    admin_logger.setLevel(logging.INFO)
    admin_logger.addHandler(stream)

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

    if not app.debug:
        sentry.app = app
        sentry.init_app(app)

    admin.app = app
    admin.init_app(app)
    admin.add_view(AdAdminView(Ad, db.session))
    admin.add_view(LinkAdminView(Link, db.session))
    admin.add_view(IssueAdminView(Issue, db.session))

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
