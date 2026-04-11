# =============================================================
#  exceptions/employee_exceptions.py
#  Custom exceptions cho hệ thống quản lý nhân viên
# =============================================================
 
class EmployeeException(Exception):
    """Base exception cho hệ thống nhân viên"""
    pass
 
 
class EmployeeNotFoundError(EmployeeException):
    """Lỗi không tìm thấy nhân viên"""
    def __init__(self, employee_id):
        self.employee_id = employee_id
        super().__init__(f"Không tìm thấy nhân viên có ID: {employee_id}")
 
 
class InvalidSalaryError(EmployeeException):
    """Lỗi lương không hợp lệ (phải > 0)"""
    def __init__(self, msg="Lương phải lớn hơn 0"):
        super().__init__(msg)
 
 
class InvalidAgeError(EmployeeException):
    """Lỗi tuổi không hợp lệ (phải 18–65)"""
    def __init__(self, msg="Tuổi phải từ 18 đến 65"):
        super().__init__(msg)
 
 
class ProjectAllocationError(EmployeeException):
    """Lỗi phân công dự án (vượt quá 5 dự án hoặc trùng)"""
    pass
 
 
class DuplicateEmployeeError(EmployeeException):
    """Lỗi trùng mã nhân viên"""
    def __init__(self, employee_id):
        self.employee_id = employee_id
        super().__init__(f"ID '{employee_id}' đã tồn tại trong hệ thống")