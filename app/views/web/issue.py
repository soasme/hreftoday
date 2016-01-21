# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect, request, abort
from flask_login import login_required, current_user
from app.models import Issue, Link, LinkTag, Tag
from app.utils.forms import populate_obj, form_required
from app.forms import TopicForm, AddIssueForm, PublishIssueForm, AddLinkForm
from app.core import db
from .core import bp

@bp.route('/topics/<int:id>/issues', defaults={'page': 1})
def get_topic_issues(id, page):
    is_published = request.args.get('is_published', type=int, default=1)
    if is_published:
        pagination = Issue.query.filter_by(topic_id=id).filter(Issue.serial != None).paginate(page)
    else:
        pagination = Issue.query.filter_by(topic_id=id, serial=None).paginate(page)
    add_issue_form = AddIssueForm()
    return render_template(
        'web/issue/list.html', pagination=pagination, add_issue_form=add_issue_form,
    )

@bp.route('/topics/<int:id>/issues', methods=['POST'])
@login_required
@form_required(AddIssueForm)
def add_issue(id):
    issue = Issue(user_id=current_user.id, topic_id=id)
    return _save_issue(issue)

@bp.route('/issues/<int:id>')
def get_issue(id):
    issue = Issue.query.get_or_404(id)
    links = Link.query.filter_by(issue_id=id).all()
    for link in links:
        link_tags = LinkTag.query.filter_by(link_id=id).order_by(LinkTag.weight.desc()).limit(10).all()
        tag_ids = [link_tag.tag_id for link_tag in link_tags]
        link.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all() if tag_ids else []
    publish_issue_form = PublishIssueForm()
    add_link_form = AddLinkForm()
    return render_template('web/issue/item.html', issue=issue, links=links, publish_issue_form=publish_issue_form, add_link_form=add_link_form)

@bp.route('/issues/<int:id>/publish')
def publish_issue_page(id):
    issue = Issue.query.get_or_404(id)
    return render_template('web/issue/publish.html', issue=issue)

@bp.route('/issues/<int:id>/publish', methods=['POST'])
def publish_issue(id):
    issue = Issue.query.get_or_404(id)
    if issue.serial:
        return abort(400)
    current_topic_max_serial = Issue.query.filter_by(topic_id=issue.topic_id).order_by(Issue.serial.desc()).with_entities(Issue.serial).scalar() or 0
    issue.serial = 1 + current_topic_max_serial
    return _save_issue(issue)

def _save_issue(issue):
    populate_obj(issue)
    return redirect(url_for('web.get_issue', id=issue.id))
