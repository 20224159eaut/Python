# =============================================================
#  exceptions/__init__.py
# =============================================================
from .employee_exceptions import (
    EmployeeException,
    EmployeeNotFoundError,
    InvalidSalaryError,
    InvalidAgeError,
    ProjectAllocationError,
    DuplicateEmployeeError,
)
 
__all__ = [
    "EmployeeException",
    "EmployeeNotFoundError",
    "InvalidSalaryError",
    "InvalidAgeError",
    "ProjectAllocationError",
    "DuplicateEmployeeError",
]
 