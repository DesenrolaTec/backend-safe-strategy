from sqlalchemy import Column, Integer, String
from app.src.infra.adapters.sql_alchemy_adapter import db

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    organization_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, primary_key=True)
    role = Column(String, nullable=True, default=None)
    client_code = Column(String, nullable=True, default=None)
    enable = Column(Integer, nullable=True, default=None)
    created_at = Column(String, nullable=True, default=None)
    updated_at = Column(String, nullable=True, default=None)

    def __str__(self):
        return self.email