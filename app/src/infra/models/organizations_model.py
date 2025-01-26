from sqlalchemy import Column, Integer, String
from app.src.infra.adapters.sql_alchemy_adapter import db

class OrganizationModel(db.Model):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, nullable=True, default=None)
    name = Column(String, nullable=True, default=None)
    owner_name = Column(String, nullable=True, default=None)
    updated_at = Column(String, nullable=True, default=None)

    def __str__(self):
        return self.owner_id