# -*- coding: utf-8 -*-

from flask import render_template
from .core import bp

@bp.errorhandler(400)
def bad_request(e):
    return render_template('web/errors/bad_request.html')
