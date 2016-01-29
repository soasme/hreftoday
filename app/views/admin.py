# -*- coding: utf-8 -*-

from flask import abort
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_user import roles_required
from app.models import Ad, Issue, Link

# Flask and Flask-SQLAlchemy initialization here

class AdminModelView(ModelView):
    can_delete = False
    page_size = 50

    def is_accessible(self):
        if not current_user.is_authenticated:
            abort(403)
        if not current_user.has_role('admin'):
            abort(403)
        return True

class AdAdminView(AdminModelView):
    column_searchable_list = ('asin', )

class IssueAdminView(AdminModelView):
    pass

class LinkAdminView(AdminModelView):
    column_auto_select_related = True
    column_select_related_list = ('links', 'issue', )
