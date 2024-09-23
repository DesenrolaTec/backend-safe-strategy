from authlib.integrations.sqla_oauth2 import OAuth2ClientMixin
from app.src.infrastructure.models.user_model import UserModel
from app.src.infrastructure.adapters.sql_alchemy_adapter import db

class OAuth2Client(db.Model, OAuth2ClientMixin):
    __tablename__ = 'oauth2_clients'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    user = db.relationship('UserModel')