from sqlalchemy import Column, Integer, String, Numeric
from app.database.connection import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    department = Column(String(100), nullable=False)
    salary = Column(Numeric(12, 2), nullable=False)
    phone_no = Column(String(10), nullable=False)
