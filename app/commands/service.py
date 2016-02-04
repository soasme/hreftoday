# -*- coding: utf-8 -*-

from flask_script import Manager
from datetime import datetime
from app.core import db
from app.models import Topic, User, Role
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

@Service.command
def add_role(name):
    role = Role(name=name)
    db.session.add(role)
    db.session.commit()
    print '%s added' % unicode(role)

@Service.command
def delete_role(name):
    role = Role.query.filter_by(name=name).first()
    if not role:
        print 'Role not found'
        exit(1)
    db.session.delete(role)
    db.session.commit()
    print 'Role %s deleted' % name
