# -*- coding: utf-8 -*-

from flask import redirect, request, render_template
from flask_login import current_user, login_required
from app.core import oauth
from .models import Client
from .core import bp


@bp.route('/token', methods=['GET', 'POST'])
@oauth.token_handler
def access_token():
    return None

@bp.route('/authorize', methods=['GET', 'POST'])
@login_required
@oauth.authorize_handler
def authorize(*args, **kwargs):
    user = current_user
    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client
        kwargs['user'] = user
        return render_template('web/oauth2/authorize.html', **kwargs)

    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'
