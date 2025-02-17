from sqlalchemy import Column, Integer, String, Text
from app.src.infra.adapters.sql_alchemy_adapter import db


class StrategiesModel(db.Model):
    __tablename__ = 'strategies'
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    organization_id = Column(Integer, nullable=False, default=None)
    name = Column(String, nullable=True, default=None)
    content = Column(Text, nullable=True, default=None)
    created_at = Column(String, nullable=True, default=None)
    updated_at = Column(String, nullable=True, default=None)