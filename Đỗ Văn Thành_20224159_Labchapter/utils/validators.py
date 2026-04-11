# =============================================================
#  utils/validators.py
#  Tất cả hàm kiểm tra / chuyển đổi dữ liệu đầu vào
# =============================================================
from exceptions.employee_exceptions import InvalidAgeError, InvalidSalaryError
 
 
def validate_age(raw: str) -> int:
    """Kiểm tra tuổi (18–65). Trả int hoặc raise."""
    try:
        age = int(raw)
    except ValueError:
        raise ValueError("Tuổi phải là số nguyên")
    if not (18 <= age <= 65):
        raise InvalidAgeError(f"Tuổi phải từ 18 đến 65 (nhận: {age})")
    return age
 
 
def validate_salary(raw: str) -> float:
    """Kiểm tra lương > 0. Trả float hoặc raise."""
    try:
        sal = float(raw.replace(",", "").replace(".", "").strip()
                    if raw.replace(",", "").replace(".", "").strip().isdigit()
                    else raw)
    except ValueError:
        raise ValueError("Lương phải là số")
    if sal <= 0:
        raise InvalidSalaryError(f"Lương phải lớn hơn 0 (nhận: {sal})")
    return sal
 
 
def validate_email(raw: str) -> str:
    """Kiểm tra email có '@'. Trả str hoặc raise."""
    raw = raw.strip()
    if "@" not in raw:
        raise ValueError(f"Email không hợp lệ – thiếu '@': {raw}")
    return raw
 
 
def validate_score(raw: str) -> float:
    """Kiểm tra điểm hiệu suất 0–10. Trả float hoặc raise."""
    try:
        score = float(raw)
    except ValueError:
        raise ValueError("Điểm phải là số (0–10)")
    if not (0 <= score <= 10):
        raise ValueError(f"Điểm phải nằm trong khoảng 0–10 (nhận: {score})")
    return score
 
 
def validate_menu_choice(raw: str, lo: int, hi: int) -> int:
    """Kiểm tra lựa chọn menu trong đoạn [lo, hi]. Trả int hoặc raise."""
    try:
        val = int(raw)
    except ValueError:
        raise ValueError(f"Vui lòng nhập số từ {lo} đến {hi}")
    if not (lo <= val <= hi):
        raise ValueError(f"Lựa chọn phải từ {lo} đến {hi} (nhận: {val})")
    return val
 
 
def validate_nonneg_int(raw: str, field: str = "Giá trị") -> int:
    """Kiểm tra số nguyên ≥ 0. Trả int hoặc raise."""
    try:
        val = int(raw)
        if val < 0:
            raise ValueError()
        return val
    except ValueError:
        raise ValueError(f"{field} phải là số nguyên không âm")