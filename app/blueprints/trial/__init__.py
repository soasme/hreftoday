# -*- coding: utf-8 -*-

from datetime import datetime
from flask import url_for, Blueprint, flash
from flask_wtf import Form
from flask_admin.contrib.sqla import ModelView
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from app.core import db
from app.utils.view import templated
from app.utils.forms import save_form_obj
from app.utils.transaction import transaction
from app.utils.user import admin_required


bp = Blueprint('trial', __name__, template_folder='templates')


class TrialEmail(db.Model):

    __tablename__ = 'trial_email'
    __table_args__ = (
        db.UniqueConstraint('email', name='uk_trial_email_email'),
    )

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)


class TrialEmailForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Apply')

class TrialEmailAdminView(ModelView):

    def is_accessible(self):
        admin_required()
        return True


@bp.route('/', methods=['GET', 'POST'])
@templated('web/trial/add.html')
@transaction(db)
def add_trial():
    trial_email = TrialEmail()
    return save_form_obj(
        db, TrialEmailForm, trial_email,
        build_next=lambda form, trial_email: url_for('trial.add_trial'),
        before_render_map=['obj->trial_email'],
        before_redirect=lambda form: flash(
            'Your email has been added to list! Please wait for our invitation email.', 'success'
        ),
    )
