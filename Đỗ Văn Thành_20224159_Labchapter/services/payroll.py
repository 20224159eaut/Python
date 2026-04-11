# =============================================================
#  services/payroll.py
#  Hàm tính lương và thống kê tài chính
# =============================================================
from models.employee  import Employee
from models.manager   import Manager
from models.developer import Developer
from models.intern    import Intern
 
 
def total_payroll(employees: list[Employee]) -> float:
    """Tổng lương toàn công ty."""
    return sum(e.calculate_salary() for e in employees)
 
 
def top_salary(employees: list[Employee], n: int = 3) -> list[Employee]:
    """Top N nhân viên lương cao nhất."""
    return sorted(employees, key=lambda e: e.calculate_salary(), reverse=True)[:n]
 
 
def salary_by_department(employees: list[Employee]) -> dict[str, float]:
    """Tổng lương gộp theo phòng ban, sắp xếp giảm dần."""
    result: dict[str, float] = {}
    for emp in employees:
        result[emp.department] = result.get(emp.department, 0.0) + emp.calculate_salary()
    return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
 
 
def count_by_type(employees: list[Employee]) -> dict[str, int]:
    """Số lượng nhân viên theo loại."""
    counts = {"Manager": 0, "Developer": 0, "Intern": 0}
    for emp in employees:
        pos = emp.get_position()
        counts[pos] = counts.get(pos, 0) + 1
    return counts
 
 
def avg_projects(employees: list[Employee]) -> float:
    """Số dự án trung bình trên mỗi nhân viên."""
    if not employees:
        return 0.0
    return sum(len(e.projects) for e in employees) / len(employees)