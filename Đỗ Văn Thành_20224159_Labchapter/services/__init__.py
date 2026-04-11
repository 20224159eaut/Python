# =============================================================
#  services/__init__.py
# =============================================================
from .company import Company
from .payroll import (
    total_payroll,
    top_salary,
    salary_by_department,
    count_by_type,
    avg_projects,
)
 
__all__ = [
    "Company",
    "total_payroll", "top_salary", "salary_by_department",
    "count_by_type", "avg_projects",
]
 