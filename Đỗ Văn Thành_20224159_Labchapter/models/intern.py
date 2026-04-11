# =============================================================
#  models/intern.py
#  Intern kế thừa Employee
#  Lương = base + phụ cấp cố định 500,000 VNĐ
# =============================================================
from models.employee import Employee
 
 
class Intern(Employee):
    """
    Thực tập sinh.
    - Phụ cấp cố định: 500,000 VNĐ / tháng
    """
 
    FIXED_ALLOWANCE = 500_000   # VNĐ
 
    def __init__(
        self,
        employee_id: str,
        name: str,
        age: int,
        email: str,
        base_salary: float,
        department: str,
        university: str  = "",
        mentor_id: str   = "",
    ):
        super().__init__(employee_id, name, age, email, base_salary, department)
        self.university = university.strip()
        self.mentor_id  = mentor_id.strip()
 
    # ── Implement abstract ────────────────────────────────────
    def calculate_salary(self) -> float:
        return self.base_salary + self.FIXED_ALLOWANCE
 
    def get_position(self) -> str:
        return "Intern"
 
    # ── Extra ─────────────────────────────────────────────────
    def __str__(self) -> str:
        return (
            super().__str__()
            + f" | Trường: {self.university or 'N/A'}"
            + f" | Mentor: {self.mentor_id or 'N/A'}"
        )