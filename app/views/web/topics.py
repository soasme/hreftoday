# -*- coding: utf-8 -*-

from flask import url_for, redirect, render_template, flash, request
from flask_login import current_user, login_required
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from app.utils.forms import save_form_obj
from app.utils.view import templated, ensure_resource, ensure_owner, redirect_to
from app.utils.transaction import transaction
from app.models import Topic, TopicFollow, Link, Ad
from app.forms import TopicForm, DeleteTopicForm
from app.core import db
from .core import bp

@bp.route('/topics', defaults={'page': 1})
@login_required
@templated('web/topic/list.html')
def get_topics(page):
    return dict(
        pagination=Topic.query.filter(
            Topic.user_id==current_user.id,
            Topic.is_deleted==False,
        ).order_by(
            Topic.created_at.desc(),
        ).paginate(page)
    )

@bp.route('/topics/add', methods=['GET', 'POST'])
@transaction(db)
@login_required
@templated('web/topic/add.html')
def add_topic():
    topic = Topic(user_id=current_user.id)
    return save_form_obj(
        db, TopicForm, topic,
        build_next=lambda form, topic: url_for('web.get_topic', id=topic.id),
        before_redirect=lambda form: flash("Topic has been added.", "success"),
    )

@bp.route('/topics/<int:id>')
@templated('web/topic/item.html')
def get_topic(id):
    topic = Topic.get_or_404(id)
    page = request.args.get('page', type=int, default=1)
    links = topic.links.order_by(Link.created_at.desc()).paginate(page)
    ads = Ad.query.order_by(func.random()).limit(3).all()
    return dict(
        topic=topic,
        links=links,
        ads=ads,
    )

@bp.route('/topics/<int:id>/update', methods=['GET', 'POST'])
@transaction(db)
@login_required
@templated('web/topic/update.html')
@ensure_resource(Topic)
def update_topic(id, topic):
    ensure_owner(topic)
    return save_form_obj(
        db,
        TopicForm,
        obj=topic,
        build_next=lambda form, topic: url_for('web.get_topic', id=id),
        before_render_map=['obj->topic'],
        before_redirect=lambda form: flash("Topic has been updated.", "success"),
    )

@bp.route('/topics/<int:id>/delete', methods=['GET', 'POST'])
@transaction(db)
@login_required
@templated('web/topic/delete.html')
@ensure_resource(Topic)
def delete_topic(id, topic):
    ensure_owner(topic)
    return save_form_obj(
        db,
        DeleteTopicForm,
        obj=topic,
        build_next=lambda form, topic: url_for('web.get_topics'),
        before_render_map=['obj->topic'],
        before_redirect=lambda form: flash("Topic has been deleted.", "success")
    )

@bp.route('/topics/<int:id>/follow')
@login_required
def follow_topic(id):
    try:
        topic = Topic.get_or_404(id)
        follow = TopicFollow(user_id=current_user.id, topic_id=topic.id)
        db.session.add(follow)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
    return redirect(url_for('web.get_topic', id=topic.id))
