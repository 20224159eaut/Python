# =============================================================
#  utils/formatters.py
#  Hàm định dạng / hiển thị thông tin ra màn hình console
# =============================================================
from models.employee  import Employee
from models.manager   import Manager
from models.developer import Developer
from models.intern    import Intern
 
# ── Hằng định dạng ────────────────────────────────────────────
W          = 64                # chiều rộng khung
SEP        = "=" * W
THIN       = "-" * W
 
 
# ── Tiêu đề / khung ───────────────────────────────────────────
def print_header(title: str):
    print(f"\n{SEP}")
    print(f"  {title}")
    print(SEP)
 
 
def print_section(title: str):
    print(f"\n{THIN}")
    print(f"  {title}")
    print(THIN)
 
 
def print_banner(company_name: str = "CÔNG TY ABC"):
    print(f"\n{SEP}")
    print(f"{'HỆ THỐNG QUẢN LÝ NHÂN VIÊN ' + company_name:^{W}}")
    print(SEP)
 
 
# ── Chi tiết 1 nhân viên ──────────────────────────────────────
def format_detail(emp: Employee) -> str:
    """Trả về chuỗi chi tiết đầy đủ của một nhân viên."""
    lines = [
        THIN,
        f"  ID           : {emp.employee_id}",
        f"  Họ và tên    : {emp.name}",
        f"  Chức vụ      : {emp.get_position()}",
        f"  Phòng ban    : {emp.department}",
        f"  Tuổi         : {emp.age}",
        f"  Email        : {emp.email}",
        f"  Lương cơ bản : {emp.base_salary:>15,.0f} VNĐ",
        f"  Tổng lương   : {emp.calculate_salary():>15,.0f} VNĐ",
        f"  Hiệu suất    : {emp.performance_score}/10",
        f"  Dự án ({len(emp.projects):>2})   : "
            + (", ".join(emp.projects) if emp.projects else "(chưa có)"),
    ]
 
    if isinstance(emp, Manager):
        lines.append(f"  Team size    : {emp.team_size} người")
    elif isinstance(emp, Developer):
        langs = ", ".join(emp.programming_languages) or "(chưa có)"
        lines += [
            f"  Ngôn ngữ    : {langs}",
            f"  Giờ OT       : {emp.overtime_hours} giờ",
        ]
    elif isinstance(emp, Intern):
        lines += [
            f"  Trường       : {emp.university or 'N/A'}",
            f"  Mentor ID    : {emp.mentor_id  or 'N/A'}",
        ]
 
    lines.append(THIN)
    return "\n".join(lines)
 
 
# ── Bảng danh sách ────────────────────────────────────────────
def _row(idx: int, emp: Employee) -> str:
    return (
        f"  {idx:>3}. [{emp.employee_id:<6}] "
        f"{emp.name:<20} {emp.get_position():<10} "
        f"{emp.department:<14} "
        f"{emp.calculate_salary():>13,.0f} VNĐ  "
        f"HS:{emp.performance_score:>4.1f}  "
        f"DA:{len(emp.projects):>2}"
    )
 
 
def print_table(employees: list, title: str = "DANH SÁCH NHÂN VIÊN"):
    print_header(title)
    if not employees:
        print("  [!] Danh sách trống.")
        return
    header = (
        f"  {'STT':>3}  {'ID':<8} {'Họ tên':<20} {'Chức vụ':<10} "
        f"{'Phòng ban':<14} {'Tổng lương':>16}   {'HS':>4}  {'DA':>3}"
    )
    print(header)
    print(f"  {THIN}")
    for i, emp in enumerate(employees, 1):
        print(_row(i, emp))
    print(f"\n  Tổng: {len(employees)} nhân viên")
 
 
# ── Tiện ích nhỏ ──────────────────────────────────────────────
def pause():
    input("\n  [ Nhấn Enter để tiếp tục... ]")
 
 
def confirm(msg: str) -> bool:
    return input(f"  {msg} (y/n): ").strip().lower() == "y"
 