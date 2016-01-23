# -*- coding: utf-8 -*-

from datetime import datetime
from urlparse import urlparse
from flask import abort
from flask_user import UserMixin
from app.core import db

class Topic(db.Model):
    __tablename__ = 'topic'
    __table_args__ = (
        db.Index('ix_user', 'user_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False, default='')
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def get_or_404(cls, id):
        topic = Topic.query.get_or_404(id)
        if topic.is_deleted:
            abort(404)
        return topic

class TopicFollow(db.Model):
    __tablename__ = 'topic_follow'
    __table_args__ = (
        db.UniqueConstraint('topic_id', 'user_id', name='ux_user_follow_topic'),
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    topic_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Issue(db.Model):
    __tablename__ = 'issue'
    __table_args__ = (
        db.UniqueConstraint('topic_id', 'serial', name='ux_topic_serial'),
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    topic_id = db.Column(db.Integer, nullable=False)
    serial = db.Column(db.Integer)
    published_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    @property
    def topic(self):
        return Topic.query.get(self.topic_id)

class Link(db.Model):
    __tablename__ = 'link'
    __table_args__ = (
        db.Index('ix_issue', 'issue_id'),
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    issue_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(1024), nullable=False)
    cover = db.Column(db.String(128))
    summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    @property
    def domain(self):
        return urlparse(self.url).hostname or self.url

class Tag(db.Model):
    __tablename__ = 'tag'
    __table_args__ = (
        db.UniqueConstraint('title', name='ux_tag_title'),
    )
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LinkTag(db.Model):
    __tablename__ = 'link_tag'
    __table_args__ = (
        db.UniqueConstraint('tag_id', 'link_id', name='ux_link_tag'),
        db.Index('ix_link', 'link_id'),
    )
    id = db.Column(db.Integer, primary_key=True)
    tag_id = db.Column(db.Integer, nullable=False)
    link_id = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserLinkTag(db.Model):
    __tablename__ = 'user_link_tag'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    link_tag_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model, UserMixin):

    __tablename__ = 'user'
    __table_args__ = (
        db.UniqueConstraint('username', name='ux_username'),
        db.UniqueConstraint('email', name='ux_email'),
        db.UniqueConstraint('mobile', name='ux_mobile'),
        db.UniqueConstraint('auth_token', name='ux_auth_token'),
    )

    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime())
    username = db.Column(db.String(64), nullable=False)
    nickname = db.Column(db.String(32), nullable=False, server_default='')
    mobile = db.Column(db.String(11))
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(128), nullable=False, server_default='')
    auth_token = db.Column(db.String(128))
    active = db.Column(db.Boolean(), nullable=False, server_default='0')
