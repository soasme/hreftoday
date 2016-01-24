# -*- coding: utf-8 -*-

from flask_script import Manager
from app.core import db
from app.models import Topic
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
