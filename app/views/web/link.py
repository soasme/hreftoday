# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect
from flask_login import current_user, login_required
from app.core import db
from app.utils.transaction import transaction
from app.utils.view import ensure_resource, templated
from app.utils.forms import save_form_obj
from app.models import Link, Issue
from app.forms import LinkForm

from .core import bp

@bp.route('/links/<int:id>')
@templated('web/link/item.html')
def get_link(id):
    link = Link.query.get_or_404(id)
    issue = link.issue
    return dict(
        link=link,
        tags=[tag for tag in link.tags],
        issue=issue,
        topic=issue.topic,
        ads=link.ads,
    )

@bp.route('/issues/<int:id>/links', methods=['GET', 'POST'])
@templated('web/link/add.html')
@transaction(db)
@login_required
@ensure_resource(Issue)
def add_issue_link(id, issue):
    link = Link(
        user_id=current_user.id,
        issue_id=issue.id
    )
    return save_form_obj(
        db, LinkForm, link,
        build_next=lambda form, link: url_for(
            'web.get_link',
            id=link.id
        )
    )

@bp.route('/links/<int:id>/update', methods=['GET', 'POST'])
@templated('web/link/update.html')
@transaction(db)
@login_required
@ensure_resource(Link)
def update_link(id, link):
    return save_form_obj(
        db, LinkForm, link,
        build_next=lambda form, link: url_for(
            'web.get_link',
            id=link.id
        ),
        before_render_map=['obj->link'],
    )
