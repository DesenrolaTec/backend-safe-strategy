from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.src.infra.adapters.sql_alchemy_adapter import db

class UserModel(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True, default=None)
    email = Column(String, nullable=True, default=None)
    password = Column(String, nullable=True, default=None)
    cpf = Column(String, nullable=True, default=None)
    birthday = Column(String, nullable=True, default=None)
    created_at = Column(String, nullable=True, default=None)
    updated_at = Column(String, nullable=True, default=None)

    def __str__(self):
        return self.email

    def get_user_id(self):
        return self.id