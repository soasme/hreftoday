# -*- coding: utf-8 -*-

from flask import render_template
from .core import bp

@bp.errorhandler(400)
def bad_request(e):
    return render_template('web/errors/bad_request.html')

@bp.app_errorhandler(404)
def not_found(e):
    return render_template('web/errors/404.html')

@bp.app_errorhandler(503)
def service_unavailable(e):
    return render_template('web/errors/503.html')
