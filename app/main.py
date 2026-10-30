from fastapi import FastAPI
from app.routes.employee import router as employee_router


# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management API",
    description="REST API for managing employee records",
    version="1.0.0"
)

app.include_router(employee_router)


@app.get("/")
def home():
    return {
        "message": "Employee Management API is running successfully using the PSQL"
    }
