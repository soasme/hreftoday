# -*- coding: utf-8 -*-

from flask import request, url_for
from app.models import Link

def get_draft_link_ids():
    return filter(None, request.args.getlist('_draft', type=int))

def get_draft_links():
    return Link.query.filter(Link.id.in_(get_draft_link_ids()))

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
    if request.args.getlist('_draft'):
        link_ids = get_draft_link_ids()
        return url_for('dashboard.get_draft_links', _draft=link_ids, _external=True)

def get_default_title():
    link_ids = get_draft_link_ids()
    if link_ids:
        title = 'Draft - ' + ','.join([link.title for link in get_draft_links()])
        return title[:128]
