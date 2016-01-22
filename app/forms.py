# -*- coding: utf-8 -*-

from app.models import Issue
from flask_wtf import Form
from wtforms import StringField, HiddenField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

class DataExisted(object):

    def __init__(self, model_class):
        self.model_class = model_class

    def __call__(self, form, field):
        id = field.data
        if not self.model_class.query.get(id):
            raise ValidationError('%s %d does not exist.' % (self.model_class.__name__, id))

class EditLinkForm(Form):
    title = StringField('title', validators=[DataRequired(), Length(max=100)])
    url = StringField('url', validators=[DataRequired(), Length(max=1024)])
    summary = TextAreaField('summary', validators=[DataRequired(), Length(min=100, max=2000)])
    submit = SubmitField('Save')

class AddLinkForm(EditLinkForm):
    issue_id = HiddenField('issue_id', validators=[DataRequired(), DataExisted(Issue)])


class TopicForm(Form):
    title = StringField('title', validators=[DataRequired(), Length(max=128)])
    description = TextAreaField('description', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Save')

class AddIssueForm(Form):
    submit = SubmitField('Add Issue')

class PublishIssueForm(Form):
    submit = SubmitField('Publish Issue')

class FollowTopicForm(Form):
    submit = SubmitField('Follow Topic')
