# -*- coding: utf-8 -*-

from flask import _app_ctx_stack as stack, abort, redirect, url_for
from functools import wraps
from sqlalchemy.exc import IntegrityError
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

def save_form_obj(db,
                  form_class,
                  obj,
                  build_next,
                  before_populate=None,
                  after_populate=None,
                  before_redirect=None,
                  before_render=None,
                  before_render_map=None,
                  on_integrity_error=None,):
    form = form_class(obj=obj)
    if form.validate_on_submit():
        if before_populate:
            before_populate(form)
        form.populate_obj(obj)
        db.session.add(obj)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            if on_integrity_error:
                on_integrity_error(form)
        if after_populate:
            after_populate(form)
        if before_redirect:
            before_redirect(form)
        return redirect(build_next(form, obj))
    data = dict(
        form=form,
        obj=obj,
    )
    if before_render:
        return before_render(data)
    if before_render_map:
        for transition in before_render_map:
            from_, to_ = [_.strip() for _ in transition.split('->')]
            data[to_] = data.pop(from_, None)
    return data
