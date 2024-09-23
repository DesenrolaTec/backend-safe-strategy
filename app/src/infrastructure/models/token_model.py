import time
from authlib.integrations.sqla_oauth2 import OAuth2TokenMixin
from app.src.infrastructure.adapters.sql_alchemy_adapter import db

class OAuth2Token(db.Model, OAuth2TokenMixin):
    __tablename__ = 'oauth2_tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('User')

    def is_refresh_token_active(self):
        if self.refresh_token_revoked_at:
            return False
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at >= time.time()