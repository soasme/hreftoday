# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect, request, g, flash
from flask_login import current_user, login_required
from app.core import db, cache
from app.utils.transaction import transaction
from app.utils.view import ensure_resource, templated
from app.utils.forms import save_form_obj
from app.forms import LinkForm
from app.models import Link, Tag, Draft

from .core import bp
from .utils import (
    get_default_link_summary, get_default_url,
    get_draft_links as _get_draft_links,
    get_default_title,
)

@bp.before_request
def before_dashboard_request():
    g.draft = Draft.query.filter_by(user_id=current_user.id).first()
    g.draft = g.draft or Draft(user_id=current_user.id)
    g.draft.links = Link.query.filter(Link.id.in_(g.draft.link_ids)).all()

@bp.route('/links/<int:id>')
@templated('web/link/item.html')
@ensure_resource(Link)
def get_link(id, link):
    return dict(link=link)

@bp.route('/links/draft')
@templated('web/link/list.html')
def get_draft_links():
    links = _get_draft_links().paginate(1)
    return dict(links=links)

@bp.route('/tags/<int:id>')
@templated('web/tag/item.html')
@ensure_resource(Tag)
def get_tag(id, tag):
    return dict(tag=tag)

@bp.route('/links/add', methods=['GET', 'POST'])
@templated('web/link/add.html')
@transaction(db)
@login_required
def add_link():
    link = Link(
        user_id=current_user.id,
        summary=get_default_link_summary(),
        url=get_default_url(),
        title=get_default_title(),
    )
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
