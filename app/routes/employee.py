from typing import Annotated
from fastapi import (APIRouter,Depends,Query,Response,status)

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.dependencies import (get_current_user,require_role)
from app.core.query_params import EmployeeQueryParams

from app.database.connection import get_db
from app.models.user import User

from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeePatch,
    EmployeeResponse,
    EmployeePageResponse
)

from app.crud import employee as employee_crud
from app.exceptions.employee_exceptions import (
    EmployeeNotFoundException,
    EmployeeAlreadyExistsException,
    InvalidEmployeeDataException
)


router = APIRouter(
    prefix="/api/v1/employees",
    tags=["Employees"]
)


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN"))
):
    try:
        return employee_crud.create_employee(db, employee_data)

    # except IntegrityError as exc:
    #     db.rollback()

    #     error_message = str(exc.orig).lower()

    #     if "email" in error_message or "duplicate entry" in error_message:
    #         detail = "An employee with this email may already exist"
    #     else:
    #         detail = "Database constraint violation. Check the submitted data."

    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail=detail
    #     ) from exc

    except IntegrityError as exc:
        db.rollback()
        raise EmployeeAlreadyExistsException() from exc


@router.get(
    "",
    response_model=EmployeePageResponse
)
def get_all_employees(
    params: Annotated[EmployeeQueryParams, Query()],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return employee_crud.get_all_employees(
        db,
        params
    )

@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    employee = employee_crud.get_employee_by_id(db, employee_id)

    # if employee is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Employee not found"
    #     )

    if employee is None:
        raise EmployeeNotFoundException(employee_id)

    

    return employee


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN"))
    
):
    try:
        employee = employee_crud.update_employee(
            db,
            employee_id,
            employee_data
        )
    # except IntegrityError as exc:
    #     db.rollback()
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT,
    #         detail="An employee with this email already exists"
    #     ) from exc

    except IntegrityError as exc:
        db.rollback()
        raise EmployeeAlreadyExistsException() from exc

    except ValueError as exc:
        raise InvalidEmployeeDataException(str(exc)) from exc

    if employee is None:
        raise EmployeeNotFoundException(employee_id)

    return employee


@router.patch(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def patch_employee(
    employee_id: int,
    employee_data: EmployeePatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN"))
):
    if not employee_data.model_fields_set:
        raise InvalidEmployeeDataException(
            "Provide at least one field to update"
        )

    try:
        employee = employee_crud.patch_employee(
            db,
            employee_id,
            employee_data
        )

    except IntegrityError as exc:
        db.rollback()
        raise EmployeeAlreadyExistsException() from exc
    
    except ValueError as exc:
        raise InvalidEmployeeDataException(str(exc)) from exc

    if employee is None:
        raise EmployeeNotFoundException(employee_id)

    return employee


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("ADMIN"))
):
    deleted = employee_crud.delete_employee(db, employee_id)

    if not deleted:
        raise EmployeeNotFoundException(employee_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
