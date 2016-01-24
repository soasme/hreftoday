# -*- coding: utf-8 -*-

from flask_login import current_user

def is_belongs_to_me(obj):
    return obj and not current_user.is_anonymous and obj.user_id == current_user.id

TESTS = {k[3:]: v for k, v in globals().items() if k.startswith('is_')}
