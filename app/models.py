from datetime import datetime
from datetime import timezone
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    """User model for db"""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))

    pastes = db.relationship('Paste', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User(id={self.id}, username={self.username}, posts={self.posts})>'


class Paste(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default="uuid_generate_v4()")
    files = db.relationship('File', backref='paste')

    user_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))


class File(db.Model):
    """Paste model for db"""
    id = db.Column(UUID(as_uuid=True), primary_key=True, default="uuid_generate_v4()")
    filename: so.Mapped[str] = so.mapped_column(default='')
    value: so.Mapped[str] = so.mapped_column()

    paste_id: so.Mapped[Optional[UUID]] = so.mapped_column(sa.ForeignKey(Paste.id), index=True)

    def __repr__(self):
        return (f'<Paste(id={self.id}, value={self.value}, timestamp={self.timestamp}'
                f'user_id={self.user_id}, author={self.author})>')
