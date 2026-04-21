import sqlite3

def run_hr_program():
    # 1. Kết nối và tạo Database trong bộ nhớ (Memory)
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Tạo bảng
    cursor.execute('''CREATE TABLE department (
                        dept_id INTEGER PRIMARY KEY, 
                        dept_name TEXT)''')
    
    cursor.execute('''CREATE TABLE employee (
                        emp_id INTEGER PRIMARY KEY, 
                        name TEXT, 
                        job TEXT, 
                        salary REAL)''')

    # Chèn dữ liệu mẫu ban đầu (Tiếng Việt)
    # Bao gồm các nhân viên ban đầu và 3 bộ dữ liệu mới theo yêu cầu
    initial_employees = [
        (1, 'NGUYỄN VĂN CLARK', 'MANAGER', 15000000),
        (2, 'LÊ THỊ MILLER', 'CLERK', 8000000),
        (3, 'TRẦN HÙNG DŨNG', 'MANAGER', 18000000),
        (4, 'PHẠM MINH TUẤN', 'DEVELOPER', 12000000), # Dữ liệu thêm 1
        (5, 'HOÀNG THU THỦY', 'ACCOUNTANT', 10000000), # Dữ liệu thêm 2
        (6, 'ĐẶNG QUỐC NAM', 'MANAGER', 20000000)      # Dữ liệu thêm 3
    ]
    cursor.executemany('INSERT INTO employee VALUES (?,?,?,?)', initial_employees)

    # ---------------------------------------------------------
    # A) Lấy ra danh sách các nhân viên có chức vụ là MANAGER
    print("--- A) DANH SÁCH NHÂN VIÊN LÀ QUẢN LÝ (MANAGER) ---")
    cursor.execute("SELECT * FROM employee WHERE job = 'MANAGER'")
    for m in cursor.fetchall():
        print(f"ID: {m[0]} | Tên: {m[1]} | Lương: {m[3]:,.0f} VNĐ")

    # B) Insert thông tin phòng làm việc thực tế
    print("\n--- B) THÊM PHÒNG LÀM VIỆC MỚI ---")
    my_dept = (101, 'Phòng Công Nghệ Thông Tin')
    cursor.execute("INSERT INTO department VALUES (?,?)", my_dept)
    print(f"Đã thêm: {my_dept[1]}")

    # C) Insert thông tin thực tế của bản thân
    print("\n--- C) THÊM THÔNG TIN BẢN THÂN VÀO HỆ THỐNG ---")
    me = (999, 'NGUYỄN TẤN TÀI', 'KỸ SƯ DỮ LIỆU', 25000000)
    cursor.execute("INSERT INTO employee VALUES (?,?,?,?)", me)
    print(f"Đã thêm nhân viên: {me[1]}")

    # D) Cập nhật thông tin của CLARK thành thông tin cá nhân của bạn
    print("\n--- D) CẬP NHẬT NHÂN VIÊN 'CLARK' THÀNH THÔNG TIN MỚI ---")
    new_info = ('NGUYỄN TẤN TÀI (ĐÃ CẬP NHẬT)', 'TRƯỞNG PHÒNG CNTT', 30000000, 'NGUYỄN VĂN CLARK')
    cursor.execute("""
        UPDATE employee 
        SET name = ?, job = ?, salary = ? 
        WHERE name = ?
    """, new_info)

    # E) Xóa thông tin của nhân viên có tên là MILLER
    print("\n--- E) XÓA NHÂN VIÊN 'MILLER' KHỎI HỆ THỐNG ---")
    cursor.execute("DELETE FROM employee WHERE name LIKE '%MILLER%'")
    print("Đã thực thi lệnh xóa.")

    # KIỂM TRA KẾT QUẢ CUỐI CÙNG
    print("\n" + "="*50)
    print(" DANH SÁCH NHÂN VIÊN SAU KHI THAY ĐỔI ")
    print("="*50)
    cursor.execute("SELECT * FROM employee")
    for row in cursor.fetchall():
        print(f"ID: {row[0]:<5} | Tên: {row[1]:<25} | Chức vụ: {row[2]:<15} | Lương: {row[3]:>12,.0f}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    run_hr_program()