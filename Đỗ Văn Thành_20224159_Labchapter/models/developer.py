# =============================================================
#  models/developer.py
#  Developer kế thừa Employee
#  Lương = base + 200,000 × số ngôn ngữ + lương OT (1.5×)
# =============================================================
from models.employee import Employee
 
 
class Developer(Employee):
    """
    Lập trình viên.
    - Phụ cấp ngôn ngữ : 200,000 VNĐ / ngôn ngữ thành thạo
    - Lương làm thêm   : lương_giờ × 1.5 × số giờ OT
                         (lương_giờ = base / 160 giờ/tháng)
    """
 
    LANG_ALLOWANCE  = 200_000   # VNĐ / ngôn ngữ
    OVERTIME_RATE   = 1.5
    HOURS_PER_MONTH = 160
 
    def __init__(
        self,
        employee_id: str,
        name: str,
        age: int,
        email: str,
        base_salary: float,
        department: str,
        programming_languages: list[str] | None = None,
        overtime_hours: int = 0,
    ):
        super().__init__(employee_id, name, age, email, base_salary, department)
        self.programming_languages: list[str] = (
            list(programming_languages) if programming_languages else []
        )
        self.overtime_hours = max(0, int(overtime_hours))
 
    # ── Implement abstract ────────────────────────────────────
    def calculate_salary(self) -> float:
        lang_allowance = len(self.programming_languages) * self.LANG_ALLOWANCE
        hourly_rate    = self.base_salary / self.HOURS_PER_MONTH
        overtime_pay   = hourly_rate * self.OVERTIME_RATE * self.overtime_hours
        return self.base_salary + lang_allowance + overtime_pay
 
    def get_position(self) -> str:
        return "Developer"
 
    # ── Extra ─────────────────────────────────────────────────
    def add_language(self, lang: str):
        """Thêm ngôn ngữ lập trình mới (không trùng)"""
        lang = lang.strip()
        if lang and lang not in self.programming_languages:
            self.programming_languages.append(lang)
 
    def __str__(self) -> str:
        langs = ", ".join(self.programming_languages) if self.programming_languages else "Chưa có"
        return super().__str__() + f" | Ngôn ngữ: [{langs}] | OT: {self.overtime_hours}h"
 