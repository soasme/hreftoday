# -*- coding: utf-8 -*-

from flask import request, url_for, g
from flask_login import current_user
from app.models import Link, Draft

def get_draft():
    return Draft.query.filter_by(user_id=current_user.id).first() or Draft(
        user_id=current_user.id
    )

def get_draft_link_ids():
    return get_draft().link_ids

def get_draft_links():
    return Link.query.filter(Link.id.in_(get_draft_link_ids()))

def get_draft_links_count():
    draft = get_draft()
    return len(set(draft.link_ids))

def get_default_link_summary():
    links = get_draft_links()
    summary = ''
    resources = []
    for link in links:
        summary += '### %s' % link.title
        summary += '\n'
        summary += '\n'
        summary += link.summary
        summary += '\n'
        summary += '\n'
        resources.append('[%s]: %s' % (link.title, link.url))
    summary += '\n'.join(resources)
    return summary

def get_default_url():
    link_ids = get_draft_link_ids()
    if link_ids:
        return url_for('dashboard.get_draft_links', _draft=link_ids, _external=True)
    else:
        return url_for('dashboard.get_links')

def get_default_title():
    link_ids = get_draft_link_ids()
    if link_ids:
        title = 'Draft - ' + ','.join([link.title for link in get_draft_links()])
        return title[:128]
    else:
        return ''
