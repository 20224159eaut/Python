# =============================================================
#  models/manager.py
#  Manager kế thừa Employee
#  Lương = base + 30% thưởng + 500,000 VNĐ × team_size
# =============================================================
from models.employee import Employee
 
 
class Manager(Employee):
    """
    Quản lý cấp cao.
    - Thưởng hiệu suất: 30% lương cơ bản
    - Phụ cấp quản lý : 500,000 VNĐ / nhân viên trực thuộc
    """
 
    BONUS_RATE       = 0.30        # 30 %
    TEAM_ALLOWANCE   = 500_000     # VNĐ / người
 
    def __init__(
        self,
        employee_id: str,
        name: str,
        age: int,
        email: str,
        base_salary: float,
        department: str,
        team_size: int = 0,
    ):
        super().__init__(employee_id, name, age, email, base_salary, department)
        self.team_size = max(0, int(team_size))
 
    # ── Implement abstract ────────────────────────────────────
    def calculate_salary(self) -> float:
        bonus          = self.base_salary * self.BONUS_RATE
        team_allowance = self.team_size   * self.TEAM_ALLOWANCE
        return self.base_salary + bonus + team_allowance
 
    def get_position(self) -> str:
        return "Manager"
 
    # ── Extra ─────────────────────────────────────────────────
    def __str__(self) -> str:
        return super().__str__() + f" | Team size: {self.team_size}"
 