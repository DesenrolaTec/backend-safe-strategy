from sqlalchemy import Column, Integer, String
from app.src.infra.adapters.sql_alchemy_adapter import db

class ActivationsHasGroupsModel(db.Model):
    __tablename__ = 'activations_has_groups'
    activations_id= Column(Integer, nullable=False)
    groups_id = Column(Integer, nullable=False)
    created_at = Column(String, nullable=True, default=None)
    updated_at = Column(String, nullable=True, default=None)
