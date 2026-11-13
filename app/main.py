from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routes.employee import router as employee_router
from app.routes.auth import router as auth_router

from app.handlers.exception_handlers import (
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    unexpected_exception_handler
)

from app.exceptions.employee_exceptions import AppException


app = FastAPI(
    title="Employee Management API",
    description="Employee Management API with Authentication, Authorization and Advanced API Features",
    version="3.0.0"
)


# Register global exception handlers

app.add_exception_handler(
    AppException,
    app_exception_handler
)

app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    unexpected_exception_handler
)


# Register API routers

app.include_router(employee_router)
app.include_router(auth_router)


@app.get("/")
def home():
    return {
        "message": "Employee Management API is running successfully using PostgreSQL"
    }