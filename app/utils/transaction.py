# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from functools import wraps
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy

def transaction(db):
    def deco(f):
        @wraps(f)
        def _(*a, **kw):
            try:
                data = f(*a, **kw)
                db.session.commit()
                return data
            except:
                db.session.rollback()
                raise
        return _
    return deco

@contextmanager
def mutex(db, Model, id):
    obj = Model.query.with_for_update().get(id)
    db.session.begin_nested()
    yield obj
    db.session.commit()

def commit_object(db):
    def deco(f):
        @wraps(f)
        def _(*args, **kwargs):
            try:
                obj = f(*args, **kwargs)
                if obj:
                    db.session.add(obj)
                db.session.commit()
                return obj
            except:
                db.session.rollback()
                raise
        return _
    return deco

def delete_object(db):
    def deco(f):
        @wraps(f)
        def _(*args, **kwargs):
            try:
                obj = f(*args, **kwargs)
                if obj:
                    db.session.delete(obj)
                db.session.commit()
            except:
                db.session.rollback()
                raise
        return _
    return deco

def delete_objects(db):
    def deco(f):
        @wraps(f)
        def _(*args, **kwargs):
            try:
                objs = f(*args, **kwargs)
                for obj in objs:
                    db.session.delete(obj)
                db.session.commit()
            except:
                db.session.rollback()
                raise
        return _
    return deco
