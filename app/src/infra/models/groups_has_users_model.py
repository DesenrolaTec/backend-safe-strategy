from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.src.infra.adapters.sql_alchemy_adapter import db

class GroupsHasUsersModel(db.Model):
    __tablename__ = 'groups_has_users'
    users_id= Column(Integer, primary_key=True, nullable=True)
    groups_id = Column(Integer, nullable=True)
    created_at = Column(String, nullable=True, default=None)
    updated_at = Column(String, nullable=True, default=None)

    __table_args__ = (
        UniqueConstraint('groups_id', 'users_id', name='uq_group_user'),
    )