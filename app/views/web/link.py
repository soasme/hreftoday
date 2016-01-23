# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect
from flask_login import current_user, login_required
from app.core import db
from app.utils.transaction import transaction
from app.utils.view import ensure_resource, templated
from app.utils.forms import save_form_obj
from app.models import Link, Tag, LinkTag, Issue
from app.forms import LinkForm

from .core import bp

@bp.route('/links/<int:id>')
def get_link(id):
    link = Link.query.get_or_404(id)
    issue = Issue.query.get_or_404(link.issue_id)
    link_tags = LinkTag.query.filter_by(link_id=id).order_by(LinkTag.weight.desc()).limit(10).all()
    tag_ids = [link_tag.tag_id for link_tag in link_tags]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all() if tag_ids else []
    return render_template('web/link/item.html', link=link, tags=tags, issue=issue)

@bp.route('/issues/<int:id>/links', methods=['GET', 'POST'])
@transaction(db)
@login_required
@templated('web/link/add.html')
@ensure_resource(Issue)
def add_issue_link(id, issue):
    link = Link(user_id=current_user.id, issue_id=issue.id)
    return save_form_obj(
        db, LinkForm, link,
        build_next=lambda form, link: url_for('web.get_link', id=link.id)
    )

@bp.route('/links/<int:id>/update', methods=['GET', 'POST'])
@transaction(db)
@login_required
@templated('web/link/update.html')
@ensure_resource(Link)
def update_link(id, link):
    return save_form_obj(
        db, LinkForm, link,
        build_next=lambda form, link: url_for('web.get_link', id=link.id),
        before_render_map=['obj->link'],
    )
