from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.database.connection import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    username = Column(String(50),unique=True,nullable=False,index=True)
    email = Column(String(255),unique=True,nullable=False,index=True)
    hashed_password = Column(String(255),nullable=False)
    role = Column(String(20),nullable=False,default="EMPLOYEE")
    is_active = Column(Boolean,nullable=False,default=True)
    created_at = Column(DateTime(timezone=True),nullable=False,server_default=func.now())