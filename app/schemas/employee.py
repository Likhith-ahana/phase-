from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    department: str = Field(min_length=1, max_length=100)
    salary: Decimal = Field(ge=0,max_digits=12,decimal_places=2)
    phone_no: str = Field(min_length=10,max_length=10,pattern=r"^[0-9]{10}$")


class EmployeeUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    department: str = Field(min_length=1, max_length=100)
    salary: Decimal = Field(ge=0,max_digits=12,decimal_places=2)
    phone_no: str = Field(min_length=10,max_length=10,pattern=r"^[0-9]{10}$")


class EmployeePatch(BaseModel):
    name: str | None = Field(default=None,min_length=1,max_length=100)
    email: EmailStr | None = None
    department: str | None = Field(default=None,min_length=1,max_length=100)
    salary: Decimal | None = Field(default=None,ge=0,max_digits=12,decimal_places=2)
    phone_no: str | None = Field(default=None,min_length=10,max_length=10,pattern=r"^[0-9]{10}$")


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
    salary: Decimal
    phone_no: str

    model_config = ConfigDict(from_attributes=True)