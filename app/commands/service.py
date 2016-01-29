# -*- coding: utf-8 -*-

from flask_script import Manager
from datetime import datetime
from app.core import db
from app.models import Topic, Issue, User, Role
from app.utils.transaction import transaction

Service = Manager('Perform service operation')

@Service.command
def revert_topic(id):
    topic = Topic.query.get(id)
    if topic:
        topic.is_deleted = False
        db.session.commit()
        print 'Topic "%s" reverted' % topic.title
    else:
        print 'Not Found'

@Service.command
def publish_issue(id):
    issue = Issue.query.get(id)
    if issue:
        latest_issue = Issue.query.filter_by(
            topic_id=issue.topic_id
        ).order_by(
            Issue.serial.desc()
        ).first()
        current_topic_max_serial = latest_issue and latest_issue.serial or 0
        issue.serial = 1 + current_topic_max_serial
        issue.published_at = datetime.utcnow()
        db.session.commit()
        print 'Issue published as serial %s' % issue.serial
    else:
        print 'Not Found'

@Service.command
def unpublish_issue(id):
    issue = Issue.query.get(id)
    if issue:
        issue.serial = None
        issue.published_at = None
        db.session.commit()
        print 'Issue unpublished'
    else:
        print 'Not Found'

@Service.command
def set_role(id, role):
    user = User.query.get(id)
    role = Role.query.filter_by(name=role).first()
    if not user:
        print 'User not found'
        exit(1)
    if not role:
        print 'Role not found'
        exit(1)
    user.roles.append(role)
    db.session.add(user)
    db.session.commit()
    print 'Role set successfully.'

@Service.command
def unset_role(id, role):
    user = User.query.get(id)
    role = Role.query.filter_by(name=role).first()
    if not user:
        print 'User not found'
        exit(1)
    if not role:
        print 'Role not found'
        exit(1)
    user.roles.remove(role)
    db.session.add(user)
    db.session.commit()
    print 'Role unset successfully.'
