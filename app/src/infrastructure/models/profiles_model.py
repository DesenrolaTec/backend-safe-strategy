from sqlalchemy import Column, Integer, String
from app.src.infrastructure.adapters.sql_alchemy_adapter import db

class ProfilesModel(db.Model):
    __tablename__ = 'profiles'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    organization_id = Column(Integer, nullable=True, default=None)
    name = Column(String, nullable=True, default=None)
    enable = Column(Integer, nullable=True, default=None)