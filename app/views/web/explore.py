# -*- coding: utf-8 -*-

from flask import render_template
from .core import bp

@bp.route('/explore')
def explore():
    return render_template('web/explore.html')
