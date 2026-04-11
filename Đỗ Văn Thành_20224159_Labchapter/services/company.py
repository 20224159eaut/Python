# =============================================================
#  services/company.py
#  Class Company – toàn bộ logic nghiệp vụ quản lý nhân viên
# =============================================================
from models.employee  import Employee
from models.manager   import Manager
from models.developer import Developer
from models.intern    import Intern
from exceptions.employee_exceptions import (
    EmployeeNotFoundError,
    DuplicateEmployeeError,
    ProjectAllocationError,
    InvalidSalaryError,
)
 
 
class Company:
    """Quản lý danh sách nhân viên và mọi nghiệp vụ liên quan."""
 
    def __init__(self, name: str = "Công ty ABC"):
        self.name = name
        self._staff: list[Employee] = []
        self._counter = 2000          # bộ đếm tự sinh ID
 
    # ══════════════════════════════════════════════════════════
    #  INTERNAL HELPERS
    # ══════════════════════════════════════════════════════════
    def _gen_id(self) -> str:
        self._counter += 1
        return f"NV{self._counter}"
 
    def _id_exists(self, eid: str) -> bool:
        return any(e.employee_id == eid for e in self._staff)
 
    def _require_nonempty(self):
        if not self._staff:
            raise IndexError("Danh sách nhân viên đang trống")
 
    # ══════════════════════════════════════════════════════════
    #  THÊM / XÓA NHÂN VIÊN
    # ══════════════════════════════════════════════════════════
    def add_employee(self, emp: Employee):
        """
        Thêm nhân viên. Nếu ID trùng → tự sinh ID mới và thông báo.
        """
        if self._id_exists(emp.employee_id):
            raise DuplicateEmployeeError(emp.employee_id)
        self._staff.append(emp)
 
    def remove_employee(self, employee_id: str) -> Employee:
        """Xóa và trả về nhân viên. Raise EmployeeNotFoundError nếu không có."""
        emp = self.find_by_id(employee_id)
        self._staff.remove(emp)
        return emp
 
    def layoff_batch(self, id_list: list[str]) -> tuple[list[Employee], list[tuple[str, str]]]:
        """
        Cắt giảm nhân sự hàng loạt.
        Trả về (success_list, [(id, reason), ...])
        """
        success, failed = [], []
        for eid in id_list:
            eid = eid.strip()
            try:
                emp = self.remove_employee(eid)
                success.append(emp)
            except EmployeeNotFoundError as exc:
                failed.append((eid, str(exc)))
        return success, failed
 
    # ══════════════════════════════════════════════════════════
    #  TÌM KIẾM
    # ══════════════════════════════════════════════════════════
    def find_by_id(self, employee_id: str) -> Employee:
        for emp in self._staff:
            if emp.employee_id == employee_id:
                return emp
        raise EmployeeNotFoundError(employee_id)
 
    def find_by_name(self, keyword: str) -> list[Employee]:
        kw = keyword.lower()
        return [e for e in self._staff if kw in e.name.lower()]
 
    def find_by_language(self, lang: str) -> list[Employee]:
        lang = lang.lower()
        return [
            e for e in self._staff
            if isinstance(e, Developer)
            and any(lang == l.lower() for l in e.programming_languages)
        ]
 
    # ══════════════════════════════════════════════════════════
    #  LẤY DANH SÁCH
    # ══════════════════════════════════════════════════════════
    def all(self) -> list[Employee]:
        return list(self._staff)
 
    def by_type(self, type_name: str) -> list[Employee]:
        mapping = {"manager": Manager, "developer": Developer, "intern": Intern}
        cls = mapping.get(type_name.lower())
        return [e for e in self._staff if cls and isinstance(e, cls)]
 
    def by_performance(self, descending: bool = True) -> list[Employee]:
        return sorted(self._staff, key=lambda e: e.performance_score, reverse=descending)
 
    def excellent(self) -> list[Employee]:
        return [e for e in self._staff if e.performance_score > 8]
 
    def needs_improvement(self) -> list[Employee]:
        return [e for e in self._staff if e.performance_score < 5]
 
    # ══════════════════════════════════════════════════════════
    #  LƯƠNG & THĂNG CHỨC
    # ══════════════════════════════════════════════════════════
    def give_raise(self, employee_id: str, amount: float) -> Employee:
        emp = self.find_by_id(employee_id)
        emp.increase_salary(amount)
        return emp
 
    def promote(self, employee_id: str) -> Employee:
        """
        Intern  → Developer  (lương × 1.5)
        Developer → Manager  (lương × 1.3)
        Manager → không thể thăng thêm
        """
        emp = self.find_by_id(employee_id)
        idx = self._staff.index(emp)
 
        if isinstance(emp, Intern):
            new_emp = Developer(
                emp.employee_id, emp.name, emp.age, emp.email,
                emp.base_salary * 1.5, emp.department,
                programming_languages=[], overtime_hours=0,
            )
        elif isinstance(emp, Developer):
            new_emp = Manager(
                emp.employee_id, emp.name, emp.age, emp.email,
                emp.base_salary * 1.3, emp.department,
                team_size=0,
            )
        else:
            raise ValueError(f"Manager '{emp.name}' đã ở chức vụ cao nhất")
 
        # Kế thừa dữ liệu
        new_emp.projects          = list(emp.projects)
        new_emp.performance_score = emp.performance_score
        self._staff[idx] = new_emp
        return new_emp
 
    # ══════════════════════════════════════════════════════════
    #  QUẢN LÝ DỰ ÁN
    # ══════════════════════════════════════════════════════════
    def assign_project(self, employee_id: str, project: str) -> Employee:
        emp = self.find_by_id(employee_id)
        emp.add_project(project)
        return emp
 
    def unassign_project(self, employee_id: str, project: str) -> Employee:
        emp = self.find_by_id(employee_id)
        emp.remove_project(project)
        return emp
 
    def all_projects(self) -> dict[str, list[Employee]]:
        """Trả về {tên_dự_án: [danh sách nhân viên]}"""
        result: dict[str, list[Employee]] = {}
        for emp in self._staff:
            for proj in emp.projects:
                result.setdefault(proj, []).append(emp)
        return result
 
    def project_members(self, project_name: str) -> list[Employee]:
        """Thành viên tham gia một dự án cụ thể."""
        return [e for e in self._staff if project_name in e.projects]
 
    def top_by_projects(self, n: int = 10, most: bool = True) -> list[Employee]:
        """Top N tham gia nhiều (most=True) hoặc ít (most=False) dự án."""
        return sorted(self._staff, key=lambda e: len(e.projects), reverse=most)[:n]
 
    # ══════════════════════════════════════════════════════════
    #  HIỆU SUẤT
    # ══════════════════════════════════════════════════════════
    def set_performance(self, employee_id: str, score: float) -> Employee:
        emp = self.find_by_id(employee_id)
        emp.update_performance(score)
        return emp
 
    # ══════════════════════════════════════════════════════════
    #  THUỘC TÍNH TIỆN ÍCH
    # ══════════════════════════════════════════════════════════
    @property
    def count(self) -> int:
        return len(self._staff)
 