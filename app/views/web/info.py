# -*- coding: utf-8 -*-

from flask import render_template, current_app, abort, make_response
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

@bp.route('/.well-known/acme-challenge/<key>')
def acme_challenge(key):
    keys = current_app.config['ACME_CHALLENGE_KEY'].split()
    if key not in keys:
        abort(404)
    values = current_app.config['ACME_CHALLENGE_VALUE'].split()
    value = values[keys.index(key)]
    resp = make_response(value)
    resp.content_type = 'text/plain'
    return resp
