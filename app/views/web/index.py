# -*- coding: utf-8 -*-

from flask import render_template
from flask_user import login_required
from .core import bp

@bp.route('/')
@login_required
def index():
    return render_template('web/index.html')
