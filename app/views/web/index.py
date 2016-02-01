# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect
from flask_user import login_required
from .core import bp

@bp.route('/')
@login_required
def index():
    return redirect(url_for('web.get_topics'))
