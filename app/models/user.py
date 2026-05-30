from datetime import datetime, timezone
from enum import Enum

from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


class Role(Enum):
    USER = 'user'
    ADMIN = 'admin'
    SUPERUSER = 'superuser'


class OAuth(OAuthConsumerMixin, db.Model):
    __tablename__ = 'oauth'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('oauth_accounts', lazy=True))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    role = db.Column(db.Enum(Role), default=Role.USER, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    password_reset_requested_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, **kwargs):
        kwargs.setdefault('role', Role.USER)
        kwargs.setdefault('is_active', True)
        super().__init__(**kwargs)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if self.password_hash is None:
            return False
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'
