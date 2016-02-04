# -*- coding: utf-8 -*-

from mistune import markdown
from datetime import datetime
from urlparse import urlparse
from flask import abort
from flask_user import UserMixin
from sqlalchemy.dialects import postgresql
from app.core import db
from app.utils.flask_amazon import amazon

class DeletableMixin(object):
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)

    @classmethod
    def get_or_404(cls, id):
        obj = cls.query.get_or_404(id)
        if obj.is_deleted:
            abort(404)
        return obj

class Topic(db.Model, DeletableMixin):
    __tablename__ = 'topic'
    __table_args__ = (
        db.Index('ix_user', 'user_id'),
        db.ForeignKeyConstraint(
            ['user_id'],
            ['user.id'],
            name='fk_topic_user',
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False, default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __unicode__(self):
        return u'Topic %d: %s' % (self.id, self.title)

class Ad(db.Model):
    __tablename__ = 'ad'
    __table_args__ = (
        db.UniqueConstraint('asin', name='ix_ad_asin'),
    )

    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(20), nullable=False)
    url = db.Column(db.String(1024), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __unicode__(self):
        return u'Ad %d %s: %s' % (self.id, self.asin, self.title)


link_ad = db.Table(
    'link_ad',
    db.Column('link_id', db.Integer, db.ForeignKey('link.id')),
    db.Column('ad_id', db.Integer, db.ForeignKey('ad.id')),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

link_tag = db.Table(
    'link_tag',
    db.Column('link_id', db.Integer, db.ForeignKey('link.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('created_at', db.DateTime, default=datetime.utcnow)
)

class TopicFollow(db.Model):
    __tablename__ = 'topic_follow'
    __table_args__ = (
        db.UniqueConstraint('topic_id', 'user_id', name='ux_topic_follow_user_follow_topic'),
        db.ForeignKeyConstraint(
            ['user_id'], ['user.id'], name='fk_topic_follow_user',
        ),
        db.ForeignKeyConstraint(
            ['topic_id'], ['topic.id'], name='fk_topic_follow_topic',
        ),
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    topic_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Link(db.Model):
    __tablename__ = 'link'
    __table_args__ = (
        db.ForeignKeyConstraint(
            ['user_id'], ['user.id'], name='fk_link_user',
        ),
        db.ForeignKeyConstraint(
            ['topic_id'], ['topic.id'], name='fk_link_topic',
        ),
    )
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    topic_id = db.Column(db.Integer)
    title = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(1024), nullable=False)
    cover = db.Column(db.String(128))
    summary = db.Column(db.Text)
    keywords = db.Column(postgresql.ARRAY(db.String(32)), default=[])
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    ads = db.relationship(
        'Ad', secondary=link_ad,
        backref=db.backref('links', lazy='dynamic'),
    )
    tags = db.relationship(
        'Tag', secondary=link_tag,
        backref=db.backref('links', lazy='dynamic'),
    )

    @property
    def domain(self):
        return urlparse(self.url).hostname or self.url

    @property
    def html_short_summary(self):
        first_line = self.summary.splitlines()[0]
        return markdown(first_line)

    @property
    def html_summary(self):
        return markdown(self.summary)

    def __unicode__(self):
        return u'Link %d: %s' % (self.id, self.title)

class Tag(db.Model):
    __tablename__ = 'tag'
    __table_args__ = (
        db.UniqueConstraint('title', name='ux_tag_title'),
    )
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
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
        db.UniqueConstraint('username', name='ux_user_username'),
        db.UniqueConstraint('email', name='ux_user_email'),
        db.UniqueConstraint('mobile', name='ux_user_mobile'),
        db.UniqueConstraint('auth_token', name='ux_user_auth_token'),
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

    roles = db.relationship(
        'Role', secondary='user_roles',
        backref=db.backref('users', lazy='dynamic')
    )
    links = db.relationship('Link', backref='links', lazy='dynamic')
    topics = db.relationship('Topic', backref='topics', lazy='dynamic')

    def __unicode__(self):
        return u'User %d: %s' % (self.id, self.username)

class UserInvitation(db.Model):
    __tablename__ = 'user_invite'
    __table_args__ = (
        db.UniqueConstraint('email', name='ux_user_invite_email'),
        db.UniqueConstraint('token', name='ux_user_invite_token'),
        db.ForeignKeyConstraint(
            ['invited_by_user_id'], ['user.id'], name='fk_user_invitation_invited_by_user',
        ),
    )
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    invited_by_user_id = db.Column(db.Integer, nullable=False)
    token = db.Column(db.String(100), nullable=False, server_default='')
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

class Role(db.Model):
    __tablename__ = 'role'
    __table_args__ = (
        db.UniqueConstraint('name', name='ux_role_name'),
    )
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))

    def __unicode__(self):
        return 'Role %d: %s' % (self.id, self.name)

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'role_id', name='uk_user_role_user_role'),
        db.ForeignKeyConstraint(
            ['user_id'], ['user.id'], ondelete='CASCADE', name='fk_user_roles_user'
        ),
        db.ForeignKeyConstraint(
            ['role_id'], ['role.id'], ondelete='CASCADE', name='fk_user_roles_role'
        ),
    )
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), nullable=False)
    role_id = db.Column(db.Integer(), nullable=False)
