from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeePatch, EmployeeUpdate


def create_employee(db: Session, employee_data: EmployeeCreate):
    employee = Employee(**employee_data.model_dump())

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


def get_all_employees(db: Session):
    statement = select(Employee).order_by(Employee.id)
    return list(db.scalars(statement).all())


def get_employee_by_id(db: Session, employee_id: int):
    statement = select(Employee).where(Employee.id == employee_id)
    return db.scalar(statement)


def update_employee(
    db: Session,
    employee_id: int,
    employee_data: EmployeeUpdate
):
    employee = get_employee_by_id(db, employee_id)

    if employee is None:
        return None

    for field, value in employee_data.model_dump().items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)

    return employee


def patch_employee(
    db: Session,
    employee_id: int,
    employee_data: EmployeePatch
):
    employee = get_employee_by_id(db, employee_id)

    if employee is None:
        return None

    changes = employee_data.model_dump(exclude_unset=True)

    for field, value in changes.items():
        if value is None:
            raise ValueError(f"{field} cannot be null")

        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)

    return employee


def delete_employee(db: Session, employee_id: int):
    employee = get_employee_by_id(db, employee_id)

    if employee is None:
        return False

    db.delete(employee)
    db.commit()

    return True
