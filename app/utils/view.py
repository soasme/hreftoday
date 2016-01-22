# -*- coding: utf-8 -*-

from functools import wraps
from flask import render_template, current_app, request, url_for, redirect, g
from werkzeug import BaseResponse

def ensure_resource(Model):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            id = kwargs.get('id') or args[0]
            resource = Model.query.get_or_404(id)
            model_name = Model.__name__.lower()
            setattr(g, model_name, resource)
            kwargs[model_name] = resource
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def redirect_to(endpoint, **kwargs):
    return redirect(url_for(endpoint, **kwargs))

def templated(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint \
                    .replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator
