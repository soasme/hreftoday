# -*- coding: utf-8 -*-

from flask import _app_ctx_stack as stack, abort
from functools import wraps
from werkzeug.local import LocalProxy


def _get_current_form():
    return getattr(stack.top, 'current_form', None)


def _load_current_form(form):
    stack.top.current_form = form


current_form = LocalProxy(_get_current_form)


def form_required(form_cls):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            form = form_cls()
            _load_current_form(form)
            if not form.validate_on_submit():
                abort(400)
                return make_error_response(form)
            return func(*args, **kwargs)
        return wrapped
    return wrapper


def revalidate_form(*errors):
    def wrapper(func):
        @wraps(func)
        def _(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors:
                current_form.validate_on_submit()
                return make_error_response(current_form)
        return _
    return wrapper

def populate_obj(obj):
    from app.core import db
    if current_form:
        current_form.populate_obj(obj)
    db.session.add(obj)
    db.session.commit()
