# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect, request, g, flash
from flask_login import current_user, login_required
from app.core import db, cache
from app.utils.transaction import transaction
from app.utils.view import ensure_resource, templated
from app.utils.forms import save_form_obj
from app.models import Link, Tag, Draft
from app.forms import LinkForm, DraftForm, DeleteDraftLinkForm

from .core import bp
from .utils import (
    get_default_link_summary, get_default_url,
    get_draft_links as _get_draft_links,
    get_default_title,
    get_draft_links_count,
)

@bp.before_request
@login_required
def before_dashboard_request():
    if current_user.is_anonymous:
        return redirect(url_for('user.login'))
    g.draft_links_count = get_draft_links_count()

@bp.route('/links/<int:id>')
@templated('web/link/item.html')
@ensure_resource(Link)
def get_link(id, link):
    add_draft = DraftForm()
    return dict(link=link, add_draft=add_draft)

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
    link = Link(user_id=current_user.id)
    return save_form_obj(
        db, LinkForm, link,
        build_next=lambda form, link: url_for('dashboard.get_link', id=link.id),
    )

@bp.route('/links/draft/add', methods=['GET', 'POST'])
@templated('web/link/draft.html')
@transaction(db)
@login_required
def add_draft():
    link = Link(
        user_id=current_user.id,
        summary=get_default_link_summary(),
        url=get_default_url(),
        title=get_default_title(),
    )
    def before_render(data):
        data['delete_draft'] = DeleteDraftLinkForm()
        data['draft_links'] = _get_draft_links()
        return data
    return save_form_obj(
        db, LinkForm, link,
        build_next=lambda form, link: url_for('dashboard.get_link', id=link.id),
        before_render=before_render,
    )

@bp.route('/links/<int:id>/update', methods=['GET', 'POST'])
@templated('web/link/update.html')
@transaction(db)
@login_required
@ensure_resource(Link)
def update_link(id, link):
    def before_render(data):
        data['delete_draft'] = DeleteDraftLinkForm()
        return data
    return save_form_obj(
        db, LinkForm, link,
        build_next=lambda form, link: url_for('dashboard.get_link', id=link.id),
        before_render_map=['obj->link'],
        before_render=before_render,
    )

@bp.route('/links/<int:id>/delete_draft', methods=['POST'])
@transaction(db)
@login_required
@ensure_resource(Link)
def remove_link_from_draft(id, link):
    draft = Draft.query.filter_by(user_id=current_user.id).first() or Draft(user_id=current_user.id)
    return save_form_obj(
        db, DeleteDraftLinkForm, draft,
        build_next=lambda form, draft: request.referrer,
        before_populate=lambda form: setattr(form, 'link_id', id),
        before_redirect=lambda form: flash(u'Removed from draft', 'danger'),
    )

@bp.route('/links/<int:id>/draft', methods=['POST'])
@transaction(db)
@login_required
@ensure_resource(Link)
def add_link_to_draft(id, link):
    draft = Draft.query.filter_by(user_id=current_user.id).first() or Draft(user_id=current_user.id)
    def append_to_draft(form):
        draft = Draft.query.filter_by(user_id=current_user.id).first()
        if id not in draft.link_ids:
            draft.link_ids.append(id)
        db.session.add(draft)
        db.session.commit()
    return save_form_obj(
        db, DraftForm, draft,
        build_next=lambda form, draft: request.referrer,
        before_populate=lambda form: setattr(form, 'link_id', id),
        before_redirect=lambda form: flash(u'Added to draft.', 'success'),
        on_integrity_error=append_to_draft,
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
