# -*- coding: utf-8 -*-

import json
from datetime import datetime
from flask import request, url_for, flash, redirect, current_app, session
from sqlalchemy.exc import IntegrityError
from flask_oauthlib.client import OAuthResponse
from flask_login import login_required, current_user
from app.core import db, pocket
from .models import PocketAuthorization
from .core import bp

def get_pocket_request_code(request_token_uri, consumer_key, redirect_uri, state=None):
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Accept': 'application/json',
    }
    payload = {
        'consumer_key': consumer_key,
        'redirect_uri': redirect_uri,
    }
    if state:
        payload['state'] = state

    resp, content = pocket.http_request(
        request_token_uri,
        headers=headers,
        data=json.dumps(payload),
        method='POST',
    )
    return OAuthResponse(resp, content)

def get_pocket_access_token(access_token_uri, consumer_key, code):
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'X-Accept': 'application/json',
    }
    payload = {
        'consumer_key': consumer_key,
        'code': code,
    }
    resp, content = pocket.http_request(
        access_token_uri,
        headers=headers,
        data=json.dumps(payload),
        method='POST',
    )
    return OAuthResponse(resp, content)

@bp.route('/pocket/login')
@login_required
def login_pocket():
    next = request.args.get('next') or request.referrer or None
    redirect_uri = url_for('social.pocket_authorized', next=next, _external=True)
    pocket_oauth_token = get_pocket_request_code(
        request_token_uri=current_app.config.get('POCKET_REQ_TOKEN_URL'),
        consumer_key=current_app.config.get('POCKET_CONSUMER_KEY'),
        redirect_uri=redirect_uri,
    )
    if pocket_oauth_token.status != 200:
        flash(u'Sorry, we cannot connect pocket server.', 'danger')
        return url_for('web.index')
    error_code = pocket_oauth_token._resp.headers.get('X-Error-Code')
    if error_code:
        flash(u'Pocket authorization flow response error %s' % error_code, 'danger')
        return url_for('web.index')
    session['pocket_request_token'] = pocket_oauth_token.data['code']
    return pocket.authorize(
        callback=redirect_uri,
        consumer_key=current_app.config.get('POCKET_CONSUMER_KEY'),
        request_token=pocket_oauth_token.data['code'],
    )

@bp.route('/pocket/authorized')
@login_required
def pocket_authorized():
    resp = get_pocket_access_token(
        access_token_uri=current_app.config.get('POCKET_ACCESS_TOKEN_URL'),
        consumer_key=current_app.config.get('POCKET_CONSUMER_KEY'),
        code=session.get('pocket_request_token')
    )
    if resp is None:
        flash(u'You denied the request to sign in.', 'danger')
        return redirect(url_for('web.index'))
    error_code = resp._resp.headers.get('X-Error-Code')
    if error_code:
        flash(u'Pocket authorization flow response error %s' % error_code, 'danger')
        return url_for('web.index')
    session.pop('pocket_request_token', None)

    username, access_token = resp.data['username'], resp.data['access_token']
    try:
        authorization = PocketAuthorization(
            user_id=current_user.id,
            username=username,
            access_token=access_token,
            authorized_at=datetime.utcnow(),
        )
        db.session.commit()
    except IntegrityError:
        authorization = PocketAuthorization.query.filter_by(user_id=current_user.id).first()
        authorization.username = username
        authorization.access_token = access_token
        authorization.authorized_at = datetime.utcnow()
        db.session.commit()
    flash(u'You have connected pocket account: %s' % username)
    return redirect(url_for('web.index'))
