from config.database import Base
from sqlalchemy import Column, String, Integer

class User(Base):

    __tablename__ = "Users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
