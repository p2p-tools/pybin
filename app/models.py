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
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))

    posts: so.WriteOnlyMapped['Paste'] = so.relationship(
        back_populates='author')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User(id={self.id}, username={self.username}, posts={self.posts})>'


class Paste(db.Model):
    """Paste model for db"""
    id = db.Column(UUID(as_uuid=True), primary_key=True, default="uuid_generate_v4()")
    value: so.Mapped[str] = so.mapped_column()
    line_count: so.Mapped[str] = so.mapped_column()
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey(User.id),
                                                         index=True)

    author: so.Mapped[Optional[User]] = so.relationship(back_populates='posts')

    def __repr__(self):
        return (f'<Paste(id={self.id}, value={self.value}, timestamp={self.timestamp}'
                f'user_id={self.user_id}, author={self.author})>')
