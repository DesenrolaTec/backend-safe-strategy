from sqlalchemy import Column, Integer, String
from app.src.infra.adapters.sql_alchemy_adapter import db

class GroupsModel(db.Model):
    __tablename__ = 'groups'
    id= Column(Integer, primary_key=True, nullable=False)
    organization_id = Column(Integer, nullable=False)
    name = Column(String, nullable=True, default=None)
    created_at = Column(String, nullable=True, default=None)
    updated_at = Column(String, nullable=True, default=None)