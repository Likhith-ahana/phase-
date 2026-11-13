from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class EmployeeQueryParams(BaseModel):

    page: int = Field(default=1, ge=1)

    limit: int = Field(default=10, ge=1, le=100)

    department: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    min_salary: Decimal | None = Field(
        default=None,
        ge=0
    )

    max_salary: Decimal | None = Field(
        default=None,
        ge=0
    )

    search: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    sort_by: Literal[
        "id",
        "name",
        "email",
        "department",
        "salary"
    ] = "id"

    order: Literal["asc", "desc"] = "asc"

    @model_validator(mode="after")
    def validate_salary_range(self):

        if (
            self.min_salary is not None
            and self.max_salary is not None
            and self.min_salary > self.max_salary
        ):
            raise ValueError(
                "min_salary cannot be greater than max_salary"
            )

        return self