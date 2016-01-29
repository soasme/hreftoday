# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import func
from flask import render_template, url_for, redirect, request, abort, flash
from flask_login import login_required, current_user
from app.models import Issue, Link, Tag, Topic
from app.utils.forms import populate_obj, form_required, save_form_obj
from app.utils.transaction import transaction
from app.utils.view import templated, ensure_resource, redirect_to, ensure_owner
from app.forms import TopicForm, IssueForm, PublishIssueForm, LinkForm
from app.core import db
from .core import bp

@bp.route('/topics/<int:id>/issues', defaults={'page': 1})
@templated('web/issue/list.html')
@ensure_resource(Topic)
def get_topic_issues(id, page, topic):
    is_published = request.args.get('is_published', type=int, default=1)
    if is_published:
        pagination = Issue.query.filter(Issue.topic_id==id, Issue.serial!=None).order_by(
            Issue.serial.desc()
        ).paginate(page)
    else:
        pagination = Issue.query.filter_by(topic_id=topic.id, serial=None).order_by(
            Issue.created_at.desc()
        ).paginate(page)
    unpublished_count = Issue.query.filter_by(
        topic_id=topic.id, serial=None).value(func.count(1))
    add_issue_form = IssueForm()
    return dict(
        is_published=is_published,
        pagination=pagination,
        unpublished_count=unpublished_count,
        add_issue_form=add_issue_form,
        topic=topic,
    )

@bp.route('/topics/<int:id>/issues/add', methods=['GET', 'POST'])
@transaction(db)
@login_required
@templated('web/issue/add.html')
@ensure_resource(Topic)
def add_topic_issue(id, topic):
    issue = Issue(user_id=current_user.id, topic_id=topic.id)
    return save_form_obj(
        db, IssueForm, issue,
        build_next=lambda form, issue: url_for('web.get_issue', id=issue.id),
    )

@bp.route('/issues/<int:id>/update', methods=['GET', 'POST'])
@templated('web/issue/update.html')
@transaction(db)
@login_required
@ensure_resource(Issue)
def update_issue(id, issue):
    return save_form_obj(
        db, IssueForm, issue,
        build_next=lambda form, issue: url_for('web.get_issue', id=issue.id),
    )

@bp.route('/issues/<int:id>')
@templated('web/issue/item.html')
def get_issue(id):
    issue = Issue.query.get_or_404(id)
    topic = issue.topic
    links = issue.links[:5]
    ads = set()
    for link in links:
        ads.update(link.ads)
    publish_issue_form = PublishIssueForm()
    add_link_form = LinkForm()
    return dict(
        issue=issue,
        links=links,
        topic=topic,
        ads=ads,
        publish_issue_form=publish_issue_form,
        add_link_form=add_link_form,
    )

@bp.route('/issues/<int:id>/publish', methods=['POST'])
@transaction(db)
@login_required
@ensure_resource(Issue)
def publish_issue(id, issue):
    ensure_owner(issue)
    if issue.serial:
        return redirect_to('web.get_issue', id=issue.id)
    if Link.query.filter_by(issue_id=id).count() < 5:
        flash('Please at least add 5 links before publishing this issue.', 'danger')
        return redirect_to('web.get_issue', id=issue.id)
    latest_issue = Issue.query.filter_by(
        topic_id=issue.topic_id
    ).order_by(
        Issue.serial.desc()
    ).first()
    current_topic_max_serial = latest_issue and latest_issue.serial or 0
    issue.serial = 1 + current_topic_max_serial
    issue.published_at = datetime.utcnow()
    return redirect_to('web.get_issue', id=issue.id)

def _save_issue(issue):
    populate_obj(issue)
    return redirect(url_for('web.get_issue', id=issue.id))
