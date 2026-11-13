from sqlalchemy.orm import Session
from sqlalchemy import select, func, or_

from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeePatch, EmployeeUpdate
from app.core.query_params import EmployeeQueryParams


def create_employee(db: Session, employee_data: EmployeeCreate):
    employee = Employee(**employee_data.model_dump())

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


# def get_all_employees(db: Session):
#     statement = select(Employee).order_by(Employee.id)
#     return list(db.scalars(statement).all())


def get_all_employees(
    db: Session,
    params: EmployeeQueryParams
):

    # Start with the Employee table
    statement = select(Employee)

    # 1. Filtering by department
    if params.department:
        statement = statement.where(
            Employee.department.ilike(params.department)
        )

    # 2. Filtering by minimum salary
    if params.min_salary is not None:
        statement = statement.where(
            Employee.salary >= params.min_salary
        )

    # 3. Filtering by maximum salary
    if params.max_salary is not None:
        statement = statement.where(
            Employee.salary <= params.max_salary
        )

    # 4. Searching by employee name or email
    if params.search:
        search_term = f"%{params.search}%"

        statement = statement.where(
            or_(
                Employee.name.ilike(search_term),
                Employee.email.ilike(search_term)
            )
        )

    # 5. Count matching records before pagination
    count_statement = select(func.count()).select_from(statement.order_by(None).subquery())

    total = db.scalar(count_statement)

    # 6. Sorting
    sort_columns = {
        "id": Employee.id,
        "name": Employee.name,
        "email": Employee.email,
        "department": Employee.department,
        "salary": Employee.salary
    }

    sort_column = sort_columns[params.sort_by]

    if params.order == "desc":
        statement = statement.order_by(sort_column.desc())
    else:
        statement = statement.order_by(sort_column.asc())

    # Add ID as a stable secondary sort
    if params.sort_by != "id":
        statement = statement.order_by(Employee.id.asc())

    # 7. Pagination
    offset = (params.page - 1) * params.limit

    statement = statement.offset(offset).limit(params.limit)

    employees = list(db.scalars(statement).all())

    # 8. Calculate total pages
    total_pages = (
    (total + params.limit - 1) // params.limit
    if total > 0 else 0
)

    return {
        "total": total,
        "page": params.page,
        "limit": params.limit,
        "total_pages": total_pages,
        "items": employees
    }

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
