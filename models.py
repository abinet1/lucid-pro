from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    
class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    post = Column(String(255))
    date = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))

