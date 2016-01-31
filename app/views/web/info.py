# -*- coding: utf-8 -*-

from flask import render_template, current_app
from .core import bp

@bp.route('/about')
def about():
    return render_template(
        'web/about.html',
    )

@bp.route('/contact')
def contact():
    return render_template(
        'web/contact.html',
        contact_email=current_app.config.get('CONTACT_EMAIL')
    )
