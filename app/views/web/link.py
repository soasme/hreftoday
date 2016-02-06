# -*- coding: utf-8 -*-

from flask import url_for, redirect
from .core import bp

@bp.route('/links/<int:id>')
def get_link(id):
    return redirect(url_for('share.get_link', id=id), 301)
