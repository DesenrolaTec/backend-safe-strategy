from app.src.infrastructure.adapters.sql_alchemy_adapter import db
from app.src.infrastructure.models.user_model import UserModel
from authlib.integrations.sqla_oauth2 import OAuth2AuthorizationCodeMixin

class OAuth2AuthorizationCode(db.Model, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'oauth2_codes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('UserModel')