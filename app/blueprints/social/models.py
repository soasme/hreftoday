# -*- coding: utf-8 -*-

from datetime import datetime
from app.core import db

class PocketAuthorization(db.Model):
    __tablename__ = 'pocket_authorization'
    __table_args__ = (
        db.UniqueConstraint('user_id', name='ux_pocket_authorization_user'),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    access_token = db.Column(db.String(40), nullable=False)
    authorized_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
