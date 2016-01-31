# -*- coding: utf-8 -*-

from flask import render_template, current_app
from .core import bp

@bp.route('/aboutus')
def aboutus():
    return render_template(
        'web/aboutus.html',
        contact_email=current_app.config.get('CONTACT_EMAIL')
    )
