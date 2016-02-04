# -*- coding: utf-8 -*-

import logging
from flask import abort, request
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_user import roles_required
from app.models import Ad, Issue, Link
from app.utils.user import admin_required

# Flask and Flask-SQLAlchemy initialization here


class AdminModelView(ModelView):
    can_delete = False
    page_size = 50

    def is_accessible(self):
        admin_required()
        return True

class AdAdminView(AdminModelView):
    column_searchable_list = ('asin', )

class LinkAdminView(AdminModelView):
    column_auto_select_related = True
    column_select_related_list = ('links', 'issue', )
