class AppException(Exception):
    """Base exception for application-specific errors."""

    def __init__(
        self,
        message: str,
        status_code: int,
        error_code: str
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

        super().__init__(message)


class EmployeeNotFoundException(AppException):

    def __init__(self, employee_id: int):
        super().__init__(
            message=f"Employee with ID {employee_id} not found",
            status_code=404,
            error_code="EMPLOYEE_NOT_FOUND"
        )


class EmployeeAlreadyExistsException(AppException):

    def __init__(self):
        super().__init__(
            message="An employee with this email already exists",
            status_code=409,
            error_code="EMPLOYEE_ALREADY_EXISTS"
        )


class InvalidEmployeeDataException(AppException):

    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=422,
            error_code="INVALID_EMPLOYEE_DATA"
        )