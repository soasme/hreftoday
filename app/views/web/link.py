# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect
from flask_login import current_user
from flask_wtf import Form
from app.models import Link, Tag, LinkTag, Issue
from app.forms import AddLinkForm, EditLinkForm
from app.utils.forms import form_required, populate_obj
from .core import bp

@bp.route('/links/<int:id>')
def get_link(id):
    link = Link.query.get_or_404(id)
    issue = Issue.query.get_or_404(link.issue_id)
    link_tags = LinkTag.query.filter_by(link_id=id).order_by(LinkTag.weight.desc()).limit(10).all()
    tag_ids = [link_tag.tag_id for link_tag in link_tags]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all() if tag_ids else []
    return render_template('web/link/item.html', link=link, tags=tags, issue=issue)

@bp.route('/issues/<int:id>/links')
def add_issue_link_page(id):
    form = AddLinkForm(data=dict(issue_id=id))
    return render_template('web/link/add.html', form=form)

@bp.route('/issues/<int:id>/links', methods=['POST'])
@form_required(AddLinkForm)
def add_issue_link(id):
    link = Link(user_id=current_user.id)
    return _save_link(link)

@bp.route('/links/<int:id>/update')
def update_link_page(id):
    link = Link.query.get_or_404(id)
    return render_template('web/link/update.html', link=link)

@bp.route('/links/<int:id>/update', methods=['POST'])
@form_required(EditLinkForm)
def update_link(id):
    link = Link.query.get_or_404(id)
    return _save_link(link)

def _save_link(link):
    populate_obj(link)
    return redirect(url_for('web.get_link', id=link.id))
