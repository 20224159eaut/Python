# =============================================================
#  models/employee.py
#  Abstract base class cho tất cả nhân viên
# =============================================================
from abc import ABC, abstractmethod
from exceptions.employee_exceptions import InvalidAgeError, InvalidSalaryError
 
 
class Employee(ABC):
    """
    Lớp cơ sở trừu tượng cho mọi loại nhân viên.
    Các lớp con BẮT BUỘC implement: calculate_salary(), get_position()
    """
 
    def __init__(
        self,
        employee_id: str,
        name: str,
        age: int,
        email: str,
        base_salary: float,
        department: str,
    ):
        self.employee_id = employee_id
        self.name        = name
        self.age         = age           # gọi setter → validate
        self.email       = email         # gọi setter → validate
        self.base_salary = base_salary   # gọi setter → validate
        self.department  = department
        self.projects: list[str] = []
        self.performance_score: float = 0.0
 
    # ── Properties với validation ────────────────────────────
    @property
    def age(self) -> int:
        return self._age
 
    @age.setter
    def age(self, value: int):
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise InvalidAgeError("Tuổi phải là số nguyên")
        if not (18 <= value <= 65):
            raise InvalidAgeError(f"Tuổi phải từ 18 đến 65 (nhận: {value})")
        self._age = value
 
    @property
    def email(self) -> str:
        return self._email
 
    @email.setter
    def email(self, value: str):
        if "@" not in str(value):
            raise ValueError(f"Email không hợp lệ (thiếu @): {value}")
        self._email = str(value).strip()
 
    @property
    def base_salary(self) -> float:
        return self._base_salary
 
    @base_salary.setter
    def base_salary(self, value: float):
        try:
            value = float(value)
        except (ValueError, TypeError):
            raise InvalidSalaryError("Lương phải là số")
        if value <= 0:
            raise InvalidSalaryError(f"Lương phải lớn hơn 0 (nhận: {value})")
        self._base_salary = value
 
    # ── Abstract methods ─────────────────────────────────────
    @abstractmethod
    def calculate_salary(self) -> float:
        """Tính tổng lương thực nhận"""
        pass
 
    @abstractmethod
    def get_position(self) -> str:
        """Trả về tên chức vụ"""
        pass
 
    # ── Quản lý dự án ────────────────────────────────────────
    def add_project(self, project_name: str):
        from exceptions.employee_exceptions import ProjectAllocationError
        if len(self.projects) >= 5:
            raise ProjectAllocationError(
                f"Nhân viên '{self.name}' đã đạt tối đa 5 dự án, "
                f"không thể thêm '{project_name}'"
            )
        if project_name in self.projects:
            raise ProjectAllocationError(
                f"Nhân viên '{self.name}' đã tham gia dự án '{project_name}' rồi"
            )
        self.projects.append(project_name)
 
    def remove_project(self, project_name: str):
        if project_name not in self.projects:
            raise ValueError(
                f"Nhân viên '{self.name}' không tham gia dự án '{project_name}'"
            )
        self.projects.remove(project_name)
 
    # ── Hiệu suất & lương ────────────────────────────────────
    def update_performance(self, score: float):
        score = float(score)
        if not (0 <= score <= 10):
            raise ValueError(f"Điểm hiệu suất phải từ 0 đến 10 (nhận: {score})")
        self.performance_score = score
 
    def increase_salary(self, amount: float):
        amount = float(amount)
        if amount <= 0:
            raise InvalidSalaryError("Số tiền tăng phải lớn hơn 0")
        self.base_salary += amount  # gọi setter → validate
 
    # ── Dunder ───────────────────────────────────────────────
    def __str__(self) -> str:
        return (
            f"[{self.employee_id}] {self.name} | {self.get_position()} | "
            f"Phòng: {self.department} | Tuổi: {self.age} | "
            f"Lương: {self.calculate_salary():,.0f} VNĐ | "
            f"Hiệu suất: {self.performance_score}/10 | "
            f"Dự án: {len(self.projects)}"
        )
 
    def __repr__(self) -> str:
        return f"<{self.get_position()} id={self.employee_id} name={self.name!r}>"
 