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
    if key != current_app.config['ACME_CHALLENGE_KEY']:
        abort(404)
    resp = make_response(current_app.config['ACME_CHALLENGE_VALUE'])
    resp.content_type = 'text/plain'
    return resp
