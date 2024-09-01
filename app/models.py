from datetime import datetime
from datetime import timezone
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
from fastnanoid import generate

from app import db
from app import Config
from app.utils import encrypt, decrypt


class User(db.Model):
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
        return f'<User(id={self.id}, username={self.username}, posts={self.pastes})>'


class Paste(db.Model):
    id: so.Mapped[str] = so.mapped_column(sa.String(9), primary_key=True, default=generate(size=9))
    files = db.relationship('File', backref='paste')

    user_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return (f'<Paste(id={self.id}, files={self.files}, timestamp={self.timestamp} '
                f'user_id={self.user_id})>')


class File(db.Model):
    """Paste model for db"""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    filename: so.Mapped[str] = so.mapped_column(default='') # maybe i should encrypt this?
    value: so.Mapped[str] = so.mapped_column()

    paste_id: so.Mapped[Optional[str]] = so.mapped_column(sa.ForeignKey(Paste.id), index=True)

    def set_value(self, value, nonce, aesgcm):
        self.value = encrypt(nonce.encode(), aesgcm, value.encode())

    def get_value(self, nonce, aesgcm):
        return decrypt(nonce.encode(), aesgcm, self.value).decode()

    def __repr__(self):
        return (f'<File(id={self.id}, filename={self.filename}, value={self.value} '
                f'paste_id={self.paste_id})>')
