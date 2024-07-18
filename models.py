from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Users(Base):
     __tablename__ = 'users'

     id = Column(Integer, primary_key=True, index=True)
     email = Column(String, unique=True)
     username = Column(String, unique=True)
     first_name = Column(String)
     last_name = Column(String)
     hashed_password = Column(String)
     is_active = Column(Boolean, default=True)
     role = Column(String)


class Students(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    address = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"))
