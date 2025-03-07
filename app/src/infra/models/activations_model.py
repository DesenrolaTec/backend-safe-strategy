from sqlalchemy import Column, Integer, String
from app.src.infra.adapters.sql_alchemy_adapter import db

class ActivationsModel(db.Model):
    __tablename__ = 'activations'
    id= Column(Integer, primary_key=True, nullable=False)
    organization_id = Column(Integer, nullable=False)
    strategy_id = Column(Integer, nullable=False)
    start_at = Column(String, nullable=True, default=None)
    stop_at = Column(String, nullable=True, default=None)
    file_url = Column(String, nullable=True, default=None)
