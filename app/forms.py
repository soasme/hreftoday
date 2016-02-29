# -*- coding: utf-8 -*-

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

class DeletableForm(Form):
    submit = SubmitField('Confirm')

    def populate_obj(self, obj):
        obj.is_deleted = True

class LinkForm(Form):
    title = StringField('title', validators=[DataRequired(), Length(max=100)])
    url = StringField('url', validators=[DataRequired(), Length(max=1024)])
    summary = TextAreaField('summary', validators=[DataRequired(), Length(min=100, max=65535)])
    submit = SubmitField('Save')


class DeleteLinkForm(DeletableForm):
    pass

class DraftForm(Form):
    submit = SubmitField('Add to draft')

    def populate_obj(self, obj):
        obj.link_ids = list(set(obj.link_ids + [self.link_id]))

class DeleteDraftLinkForm(Form):
    submit = SubmitField('Delete from draft')

    def populate_obj(self, obj):
        if not obj:
            return
        link_ids = set(obj.link_ids)
        if self.link_id in link_ids:
            link_ids.remove(self.link_id)
        obj.link_ids = list(link_ids)
