# -*- coding: utf-8 -*-

import logging
from flask import abort, request
from flask_login import current_user

def admin_required():
    admin_logger = logging.getLogger('app.admin')
    if not current_user.is_authenticated:
        admin_logger.warning(
            'an atempting entering from unauthenticated user: %s',
            request.remote_addr,
        )
        abort(403)
    if not current_user.has_role('admin'):
        admin_logger.warning(
            'an atempting entering from non-permissive user: %s',
            current_user.id
        )
        abort(403)
