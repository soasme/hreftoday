# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect, request
from flask_login import current_user, login_required
from app.core import db, cache
from app.utils.transaction import transaction
from app.utils.view import ensure_resource, templated
from app.utils.forms import save_form_obj
from app.models import Link, Topic
from app.forms import LinkForm

from .core import bp

@bp.route('/links/<int:id>')
@templated('web/link/item.html')
def get_link(id):
    link = Link.query.get_or_404(id)
    return dict(
        link=link,
        tags=[tag for tag in link.tags],
        ads=link.ads,
    )

@bp.route('/links/add', methods=['GET', 'POST'])
@templated('web/link/add.html')
@transaction(db)
@login_required
def add_link():
    link = Link(user_id=current_user.id)
    return save_form_obj(
        db, LinkForm, link,
        build_next=lambda form, link: url_for('dashboard.get_link', id=link.id)
    )

@bp.route('/links/<int:id>/update', methods=['GET', 'POST'])
@templated('web/link/update.html')
@transaction(db)
@login_required
@ensure_resource(Link)
def update_link(id, link):
    return save_form_obj(
        db, LinkForm, link,
        build_next=lambda form, link: url_for('dashboard.get_link', id=link.id),
        before_render_map=['obj->link'],
    )


@bp.route('/')
@bp.route('/links')
@templated('web/link/list.html')
@login_required
def get_links():
    page = request.args.get('page', type=int, default=1)
    links = current_user.links.order_by(Link.created_at.desc()).paginate(page)
    return dict(
        links=links,
    )

@bp.route('/tags')
def get_tags():
    return {}
