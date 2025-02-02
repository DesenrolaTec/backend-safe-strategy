from sqlalchemy import Column, Integer, String
from app.src.infra.adapters.sql_alchemy_adapter import db

class GroupsHasUsersModel(db.Model):
    __tablename__ = 'groups_has_users'
    groups_id = Column(Integer, nullable=True)
    users_id= Column(Integer, nullable=True)
    created_at = Column(String, nullable=True, default=None)
    updated_at = Column(String, nullable=True, default=None)