# =============================================================
#  main.py  –  Chương trình chính
#  Chạy:  python main.py   (từ thư mục employee_management/)
# =============================================================
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
 
from models    import Manager, Developer, Intern
from services  import (Company, total_payroll, top_salary,
                       salary_by_department, count_by_type, avg_projects)
from utils     import (validate_age, validate_salary, validate_email,
                       validate_score, validate_menu_choice, validate_nonneg_int,
                       print_header, print_section, print_banner,
                       format_detail, print_table, pause, confirm, SEP, THIN)
from exceptions import (EmployeeNotFoundError, InvalidSalaryError,
                        InvalidAgeError, ProjectAllocationError,
                        DuplicateEmployeeError)
 
# ══════════════════════════════════════════════════════════════
#  HELPER NHẬP LIỆU
# ══════════════════════════════════════════════════════════════
MAX_TRIES = 5
 
def ask(prompt: str, validator, tries: int = MAX_TRIES):
    """Hỏi liên tục tối đa `tries` lần cho đến khi hợp lệ."""
    for attempt in range(tries):
        try:
            return validator(input(f"  {prompt}").strip())
        except (ValueError, InvalidAgeError, InvalidSalaryError) as exc:
            print(f"  [!] {exc}")
            if attempt == tries - 1:
                print("  [!] Đã vượt quá số lần nhập. Quay lại menu.\n")
                return None
    return None
 
def ask_str(prompt: str, min_len: int = 1) -> str | None:
    """Nhập chuỗi không rỗng."""
    for _ in range(MAX_TRIES):
        val = input(f"  {prompt}").strip()
        if len(val) >= min_len:
            return val
        print(f"  [!] Không được để trống.")
    print("  [!] Quá số lần nhập.\n")
    return None
 
def choose(prompt: str, lo: int, hi: int) -> int | None:
    return ask(prompt, lambda s: validate_menu_choice(s, lo, hi))
 
 
# ══════════════════════════════════════════════════════════════
#  DỮ LIỆU MẪU
# ══════════════════════════════════════════════════════════════
def load_sample(company: Company):
    from exceptions.employee_exceptions import ProjectAllocationError
    raw = [
        Manager  ("NV1001","Nguyễn Văn An",   35,"an@abc.vn",    20_000_000,"Ban Giám Đốc",team_size=5),
        Manager  ("NV1002","Trần Thị Bích",   40,"bich@abc.vn",  18_000_000,"IT",          team_size=3),
        Developer("NV1003","Lê Văn Cường",    28,"cuong@abc.vn", 15_000_000,"IT",
                  programming_languages=["Python","JavaScript"], overtime_hours=10),
        Developer("NV1004","Phạm Thị Dung",   26,"dung@abc.vn",  13_000_000,"IT",
                  programming_languages=["Java","Kotlin","SQL"], overtime_hours=5),
        Developer("NV1005","Hoàng Minh Em",   30,"em@abc.vn",    14_000_000,"IT",
                  programming_languages=["C++","Python"],        overtime_hours=0),
        Intern   ("NV1006","Vũ Thị Phương",   21,"phuong@abc.vn", 4_000_000,"HR",
                  university="ĐH Bách Khoa HN", mentor_id="NV1001"),
        Intern   ("NV1007","Đinh Văn Quân",   22,"quan@abc.vn",   3_500_000,"IT",
                  university="ĐH Công Nghệ",    mentor_id="NV1003"),
        Developer("NV1008","Bùi Thị Hoa",     27,"hoa@abc.vn",  12_000_000,"Marketing",
                  programming_languages=["Python","R"],          overtime_hours=8),
    ]
    scores   = [9.2, 8.5, 7.8, 6.5, 8.9, 5.2, 4.0, 7.1]
    proj_map = [
        ["Alpha","Beta","Gamma"],
        ["Alpha","Delta"],
        ["Beta","Gamma","Epsilon"],
        ["Delta","Epsilon"],
        ["Alpha","Gamma"],
        ["Beta"],
        [],
        ["Zeta","Alpha","Beta"],
    ]
    for emp, sc, projs in zip(raw, scores, proj_map):
        company.add_employee(emp)
        emp.performance_score = sc
        for p in projs:
            try: emp.add_project(p)
            except ProjectAllocationError: pass
 
 
# ══════════════════════════════════════════════════════════════
#  NHÓM 1 – THÊM NHÂN VIÊN
# ══════════════════════════════════════════════════════════════
def _common_fields() -> dict | None:
    """Nhập các trường dùng chung cho mọi loại nhân viên."""
    eid  = ask_str("Nhập ID nhân viên (VD: NV2001): ")
    if not eid: return None
    name = ask_str("Họ và tên                     : ")
    if not name: return None
    age  = ask("Tuổi (18–65)                  : ", validate_age)
    if age  is None: return None
    mail = ask("Email                         : ", validate_email)
    if mail is None: return None
    sal  = ask("Lương cơ bản (VNĐ)            : ", validate_salary)
    if sal  is None: return None
    dept = ask_str("Phòng ban                     : ")
    if not dept: return None
    return dict(id=eid, name=name, age=age, email=mail, salary=sal, dept=dept)
 
def _try_add(company: Company, emp):
    try:
        company.add_employee(emp)
        print(f"\n  [✓] Đã thêm {emp.get_position()}: {emp.name} (ID: {emp.employee_id})\n")
    except DuplicateEmployeeError as exc:
        print(f"  [!] {exc}")
        new_id = company._gen_id()
        emp.employee_id = new_id
        company.add_employee(emp)
        print(f"  [i] Tự động cấp ID mới: {new_id}\n")
 
def add_manager(company: Company):
    print_section("THÊM MANAGER")
    f = _common_fields()
    if not f: return
    ts = ask("Số nhân viên quản lý          : ", lambda s: validate_nonneg_int(s,"Số NV")) or 0
    _try_add(company, Manager(f["id"],f["name"],f["age"],f["email"],f["salary"],f["dept"],team_size=ts))
 
def add_developer(company: Company):
    print_section("THÊM DEVELOPER")
    f = _common_fields()
    if not f: return
    raw_langs = input("  Ngôn ngữ lập trình (phẩy)    : ").strip()
    langs = [l.strip() for l in raw_langs.split(",") if l.strip()]
    ot = ask("Số giờ OT trong tháng         : ", lambda s: validate_nonneg_int(s,"Giờ OT")) or 0
    _try_add(company, Developer(f["id"],f["name"],f["age"],f["email"],f["salary"],f["dept"],
                                programming_languages=langs, overtime_hours=ot))
 
def add_intern(company: Company):
    print_section("THÊM INTERN")
    f = _common_fields()
    if not f: return
    uni    = input("  Tên trường đại học           : ").strip()
    mentor = input("  ID Mentor (Enter nếu chưa có): ").strip()
    _try_add(company, Intern(f["id"],f["name"],f["age"],f["email"],f["salary"],f["dept"],
                             university=uni, mentor_id=mentor))
 
def menu_add(company: Company):
    print_header("THÊM NHÂN VIÊN MỚI")
    print("  a. Thêm Manager\n  b. Thêm Developer\n  c. Thêm Intern")
    ch = input("  Chọn loại (a/b/c): ").strip().lower()
    {"a": add_manager, "b": add_developer, "c": add_intern}.get(ch, lambda _: print("  [!] Không hợp lệ."))(company)
 
 
# ══════════════════════════════════════════════════════════════
#  NHÓM 2 – HIỂN THỊ
# ══════════════════════════════════════════════════════════════
def menu_display(company: Company):
    print_header("HIỂN THỊ DANH SÁCH")
    print("  a. Tất cả nhân viên\n  b. Theo loại\n  c. Theo hiệu suất (cao → thấp)")
    ch = input("  Chọn (a/b/c): ").strip().lower()
 
    if ch == "a":
        emps = company.all()
        if not emps: print("  [!] Chưa có dữ liệu."); return
        print_table(emps, "TẤT CẢ NHÂN VIÊN")
 
    elif ch == "b":
        print("  Nhập loại: manager / developer / intern")
        t = input("  ").strip()
        emps = company.by_type(t)
        if not emps: print(f"  [!] Không có nhân viên loại '{t}'."); return
        print_table(emps, f"DANH SÁCH {t.upper()}")
 
    elif ch == "c":
        emps = company.by_performance()
        if not emps: print("  [!] Chưa có dữ liệu."); return
        print_table(emps, "THEO HIỆU SUẤT (CAO → THẤP)")
 
    else:
        print("  [!] Không hợp lệ.")
 
 
# ══════════════════════════════════════════════════════════════
#  NHÓM 3 – TÌM KIẾM
# ══════════════════════════════════════════════════════════════
def menu_search(company: Company):
    print_header("TÌM KIẾM NHÂN VIÊN")
    print("  a. Theo ID\n  b. Theo tên\n  c. Theo ngôn ngữ lập trình (Developer)")
    ch = input("  Chọn (a/b/c): ").strip().lower()
    try:
        if ch == "a":
            eid = ask_str("Nhập ID: ")
            if eid: print(format_detail(company.find_by_id(eid)))
 
        elif ch == "b":
            kw = ask_str("Nhập tên (một phần): ")
            if kw:
                res = company.find_by_name(kw)
                if not res: print(f"  [!] Không tìm thấy '{kw}'.")
                else: print_table(res, f"KẾT QUẢ: '{kw}'")
 
        elif ch == "c":
            lang = ask_str("Nhập ngôn ngữ: ")
            if lang:
                res = company.find_by_language(lang)
                if not res: print(f"  [!] Không có Developer biết '{lang}'.")
                else: print_table(res, f"DEVELOPER BIẾT '{lang}'")
 
        else:
            print("  [!] Không hợp lệ.")
 
    except EmployeeNotFoundError as exc:
        print(f"  [!] {exc}")
 
 
# ══════════════════════════════════════════════════════════════
#  NHÓM 4 – LƯƠNG
# ══════════════════════════════════════════════════════════════
def menu_salary(company: Company):
    print_header("QUẢN LÝ LƯƠNG")
    print("  a. Lương của một nhân viên\n  b. Tổng lương công ty\n  c. Top 3 lương cao nhất")
    ch = input("  Chọn (a/b/c): ").strip().lower()
 
    try:
        if ch == "a":
            eid = ask_str("Nhập ID: ")
            if not eid: return
            emp = company.find_by_id(eid)
            print(f"\n  {THIN}")
            print(f"  Nhân viên  : {emp.name} ({emp.get_position()})")
            print(f"  Lương CB   : {emp.base_salary:>15,.0f} VNĐ")
            print(f"  Tổng lương : {emp.calculate_salary():>15,.0f} VNĐ")
            print(f"  {THIN}")
 
        elif ch == "b":
            emps = company.all()
            if not emps: print("  [!] Chưa có dữ liệu."); return
            print(f"\n  Tổng NV    : {len(emps)}")
            print(f"  Tổng lương : {total_payroll(emps):>15,.0f} VNĐ")
 
        elif ch == "c":
            emps = company.all()
            if not emps: print("  [!] Chưa có dữ liệu."); return
            print_section("TOP 3 LƯƠNG CAO NHẤT")
            for i, e in enumerate(top_salary(emps, 3), 1):
                print(f"  {i}. {e.name:<22} ({e.get_position():<10}) "
                      f"→ {e.calculate_salary():>14,.0f} VNĐ")
        else:
            print("  [!] Không hợp lệ.")
 
    except EmployeeNotFoundError as exc:
        print(f"  [!] {exc}")
 
 
# ══════════════════════════════════════════════════════════════
#  NHÓM 5 – DỰ ÁN
# ══════════════════════════════════════════════════════════════
def menu_project(company: Company):
    print_header("QUẢN LÝ DỰ ÁN")
    print("  a. Phân công nhân viên vào dự án")
    print("  b. Xóa nhân viên khỏi dự án")
    print("  c. Hiển thị dự án của 1 nhân viên")
    print("  d. Top 10 tham gia NHIỀU dự án nhất")
    print("  e. Top 10 tham gia ÍT  dự án nhất")
    print("  f. Danh sách thành viên 1 dự án + chức vụ")
    ch = input("  Chọn (a-f): ").strip().lower()
 
    try:
        if ch == "a":
            eid  = ask_str("Nhập ID nhân viên: ")
            if not eid: return
            proj = ask_str("Nhập tên dự án   : ")
            if not proj: return
            emp = company.assign_project(eid, proj)
            print(f"  [✓] {emp.name} → dự án '{proj}' (hiện {len(emp.projects)}/5)")
 
        elif ch == "b":
            eid  = ask_str("Nhập ID nhân viên: ")
            if not eid: return
            proj = ask_str("Nhập tên dự án   : ")
            if not proj: return
            emp = company.unassign_project(eid, proj)
            print(f"  [✓] Đã xóa {emp.name} khỏi dự án '{proj}'")
 
        elif ch == "c":
            eid = ask_str("Nhập ID nhân viên: ")
            if not eid: return
            emp = company.find_by_id(eid)
            print(f"\n  Nhân viên : {emp.name}")
            if emp.projects:
                for i, p in enumerate(emp.projects, 1):
                    print(f"    {i}. {p}")
            else:
                print("  (chưa tham gia dự án nào)")
 
        elif ch == "d":
            lst = company.top_by_projects(10, most=True)
            if not lst: print("  [!] Chưa có dữ liệu."); return
            print_section("TOP 10 THAM GIA NHIỀU DỰ ÁN NHẤT")
            _print_project_rank(lst)
 
        elif ch == "e":
            lst = company.top_by_projects(10, most=False)
            if not lst: print("  [!] Chưa có dữ liệu."); return
            print_section("TOP 10 THAM GIA ÍT DỰ ÁN NHẤT")
            _print_project_rank(lst)
 
        elif ch == "f":
            pname = ask_str("Nhập tên dự án: ")
            if not pname: return
            members = company.project_members(pname)
            if not members:
                print(f"  [!] Không có thành viên nào trong dự án '{pname}'.")
                return
            print_section(f"THÀNH VIÊN DỰ ÁN: {pname.upper()}")
            print(f"  {'STT':>3}  {'ID':<8} {'Họ tên':<22} {'Chức vụ':<12} Phòng ban")
            print(f"  {THIN}")
            for i, emp in enumerate(members, 1):
                print(f"  {i:>3}.  {emp.employee_id:<8} {emp.name:<22} "
                      f"{emp.get_position():<12} {emp.department}")
            print(f"\n  Tổng: {len(members)} thành viên")
 
        else:
            print("  [!] Không hợp lệ.")
 
    except (EmployeeNotFoundError, ProjectAllocationError, ValueError) as exc:
        print(f"  [!] {exc}")
 
def _print_project_rank(lst):
    for i, emp in enumerate(lst, 1):
        bar = "█" * len(emp.projects) if emp.projects else "–"
        print(f"  {i:>2}. [{emp.employee_id}] {emp.name:<22} "
              f"({emp.get_position():<10}) | {len(emp.projects):>2} DA  {bar}")
 
 
# ══════════════════════════════════════════════════════════════
#  NHÓM 6 – HIỆU SUẤT
# ══════════════════════════════════════════════════════════════
def menu_performance(company: Company):
    print_header("ĐÁNH GIÁ HIỆU SUẤT")
    print("  a. Cập nhật điểm hiệu suất\n  b. Nhân viên xuất sắc (> 8)\n  c. Cần cải thiện (< 5)")
    ch = input("  Chọn (a/b/c): ").strip().lower()
 
    try:
        if ch == "a":
            eid   = ask_str("Nhập ID: ")
            if not eid: return
            score = ask("Điểm hiệu suất (0–10): ", validate_score)
            if score is None: return
            emp = company.set_performance(eid, score)
            print(f"  [✓] Cập nhật điểm {score} cho {emp.name}")
 
        elif ch == "b":
            lst = company.excellent()
            if not lst: print("  [!] Không có ai điểm > 8."); return
            print_table(lst, "NHÂN VIÊN XUẤT SẮC (> 8)")
 
        elif ch == "c":
            lst = company.needs_improvement()
            if not lst: print("  [!] Không có ai điểm < 5."); return
            print_table(lst, "CẦN CẢI THIỆN (< 5)")
 
        else:
            print("  [!] Không hợp lệ.")
 
    except (EmployeeNotFoundError, ValueError) as exc:
        print(f"  [!] {exc}")
 
 
# ══════════════════════════════════════════════════════════════
#  NHÓM 7 – NHÂN SỰ
# ══════════════════════════════════════════════════════════════
def menu_hr(company: Company):
    print_header("QUẢN LÝ NHÂN SỰ")
    print("  a. Xóa nhân viên (nghỉ việc)")
    print("  b. Tăng lương cơ bản")
    print("  c. Thăng chức (Intern→Dev, Dev→Manager)")
    print("  d. Cắt giảm nhân sự hàng loạt")
    ch = input("  Chọn (a/b/c/d): ").strip().lower()
 
    try:
        if ch == "a":
            eid = ask_str("Nhập ID cần xóa: ")
            if not eid: return
            emp = company.find_by_id(eid)
            if not confirm(f"Xác nhận xóa '{emp.name}' ({emp.get_position()})?"):
                print("  [i] Đã hủy."); return
            company.remove_employee(eid)
            print(f"  [✓] Đã xóa {emp.name}. Còn lại: {company.count} nhân viên.")
 
        elif ch == "b":
            eid    = ask_str("Nhập ID: ")
            if not eid: return
            amount = ask("Số tiền tăng (VNĐ): ", validate_salary)
            if amount is None: return
            emp = company.give_raise(eid, amount)
            print(f"  [✓] {emp.name}: lương CB mới = {emp.base_salary:,.0f} VNĐ")
 
        elif ch == "c":
            eid = ask_str("Nhập ID: ")
            if not eid: return
            emp = company.find_by_id(eid)
            if not confirm(f"Thăng chức '{emp.name}' từ {emp.get_position()}?"):
                print("  [i] Đã hủy."); return
            old = emp.get_position()
            new_emp = company.promote(eid)
            print(f"  [✓] {new_emp.name}: {old} → {new_emp.get_position()} "
                  f"| Lương CB mới: {new_emp.base_salary:,.0f} VNĐ")
 
        elif ch == "d":
            _layoff(company)
 
        else:
            print("  [!] Không hợp lệ.")
 
    except (EmployeeNotFoundError, InvalidSalaryError, ValueError) as exc:
        print(f"  [!] {exc}")
 
def _layoff(company: Company):
    """Cắt giảm hàng loạt."""
    print_section("CẮT GIẢM NHÂN SỰ HÀNG LOẠT")
    emps = company.all()
    if not emps:
        print("  [!] Chưa có nhân viên."); return
 
    # Hiện danh sách tham khảo
    print(f"  Hiện có {company.count} nhân viên:")
    for e in emps:
        print(f"    [{e.employee_id}] {e.name:<22} ({e.get_position():<10}) "
              f"HS:{e.performance_score:>4.1f}")
 
    print("\n  Nhập các ID cần cắt giảm, phân cách bằng dấu phẩy.")
    print("  VD: NV1003,NV1005,NV1007")
    raw = input("  ID cần cắt giảm: ").strip()
    if not raw:
        print("  [i] Không có ID nào. Quay lại."); return
 
    ids = [i.strip() for i in raw.split(",") if i.strip()]
    print(f"\n  Danh sách sẽ bị cắt giảm ({len(ids)} người):")
    for i in ids: print(f"    - {i}")
    if not confirm("Xác nhận cắt giảm?"):
        print("  [i] Đã hủy."); return
 
    ok, fail = company.layoff_batch(ids)
    print_section("KẾT QUẢ CẮT GIẢM")
    if ok:
        print(f"  [✓] Thành công ({len(ok)} người):")
        for e in ok:
            print(f"      - [{e.employee_id}] {e.name} ({e.get_position()})")
    if fail:
        print(f"\n  [!] Không xử lý được ({len(fail)} ID):")
        for eid, reason in fail:
            print(f"      - {eid}: {reason}")
    print(f"\n  Còn lại trong công ty: {company.count} nhân viên")
 
 
# ══════════════════════════════════════════════════════════════
#  NHÓM 8 – THỐNG KÊ
# ══════════════════════════════════════════════════════════════
def menu_stats(company: Company):
    print_header("THỐNG KÊ BÁO CÁO")
    print("  a. Số lượng NV theo loại\n  b. Tổng lương theo phòng ban\n  c. Thống kê dự án")
    ch = input("  Chọn (a/b/c): ").strip().lower()
 
    emps = company.all()
    if not emps:
        print("  [!] Chưa có dữ liệu."); return
 
    if ch == "a":
        counts = count_by_type(emps)
        total  = company.count
        print_section("SỐ LƯỢNG THEO LOẠI")
        for pos, cnt in counts.items():
            pct = cnt / total * 100 if total else 0
            bar = "█" * cnt
            print(f"  {pos:<12}: {cnt:>3} người  ({pct:>5.1f} %)  {bar}")
        print(f"  {'─'*40}")
        print(f"  {'Tổng':<12}: {total:>3} người")
 
    elif ch == "b":
        dept_sal = salary_by_department(emps)
        grand    = total_payroll(emps)
        print_section("TỔNG LƯƠNG THEO PHÒNG BAN")
        for dept, sal in dept_sal.items():
            pct = sal / grand * 100 if grand else 0
            print(f"  {dept:<20}: {sal:>15,.0f} VNĐ  ({pct:>5.1f} %)")
        print(f"  {'─'*40}")
        print(f"  {'Tổng cộng':<20}: {grand:>15,.0f} VNĐ")
 
    elif ch == "c":
        all_proj = company.all_projects()
        print_section("THỐNG KÊ DỰ ÁN")
        print(f"  Số DA trung bình / NV: {avg_projects(emps):.2f}")
        print(f"  Tổng DA khác nhau    : {len(all_proj)}")
        if all_proj:
            big   = max(all_proj, key=lambda p: len(all_proj[p]))
            small = min(all_proj, key=lambda p: len(all_proj[p]))
            print(f"  DA nhiều thành viên  : '{big}'  ({len(all_proj[big])} người)")
            print(f"  DA ít  thành viên    : '{small}'  ({len(all_proj[small])} người)")
        if not any(e.projects for e in emps):
            print("  (Chưa có nhân viên nào được phân công dự án)")
    else:
        print("  [!] Không hợp lệ.")
 
 
# ══════════════════════════════════════════════════════════════
#  MENU CHÍNH
# ══════════════════════════════════════════════════════════════
MENU_ITEMS = [
    "1. Thêm nhân viên mới",
    "2. Hiển thị danh sách nhân viên",
    "3. Tìm kiếm nhân viên",
    "4. Quản lý lương",
    "5. Quản lý dự án",
    "6. Đánh giá hiệu suất",
    "7. Quản lý nhân sự",
    "8. Thống kê báo cáo",
    "9. Thoát",
]
 
HANDLERS = {
    1: menu_add,
    2: menu_display,
    3: menu_search,
    4: menu_salary,
    5: menu_project,
    6: menu_performance,
    7: menu_hr,
    8: menu_stats,
}
 
def print_main_menu(company_name: str):
    print(f"\n{SEP}")
    print(f"{'HỆ THỐNG QUẢN LÝ NHÂN VIÊN ' + company_name:^64}")
    print(SEP)
    for item in MENU_ITEMS:
        print(f"  {item}")
    print(SEP)
 
 
def main():
    company = Company("CÔNG TY ABC")
 
    # Màn hình chào
    print(f"\n{SEP}")
    print(f"{'CHÀO MỪNG ĐẾN HỆ THỐNG QUẢN LÝ NHÂN VIÊN':^64}")
    print(SEP)
    if confirm("Tải dữ liệu mẫu để trải nghiệm nhanh?"):
        load_sample(company)
        print(f"  [✓] Đã tải {company.count} nhân viên mẫu.\n")
 
    while True:
        print_main_menu(company.name)
        choice = choose("Chọn chức năng (1-9): ", 1, 9)
        if choice is None:
            continue
        if choice == 9:
            print(f"\n  Cảm ơn đã sử dụng hệ thống. Tạm biệt!\n")
            break
        try:
            HANDLERS[choice](company)
        except IndexError:
            print("  [!] Danh sách trống.")
        except Exception as exc:
            print(f"  [!] Lỗi không mong đợi: {exc}")
        pause()
 
 
if __name__ == "__main__":
    main()