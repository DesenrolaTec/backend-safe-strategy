from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True, default=None)
    email = Column(String, nullable=True, default=None)
    password = Column(String, nullable=True, default=None)
    cpf = Column(String, nullable=True, default=None)
    birthday = Column(String, nullable=True, default=None)