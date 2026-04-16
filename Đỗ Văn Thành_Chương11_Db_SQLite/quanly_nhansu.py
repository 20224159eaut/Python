import sqlite3

# ===== Kết nối database =====
conn = sqlite3.connect("nhansu.db")
cursor = conn.cursor()

# ===== Tạo bảng =====
cursor.execute("""
CREATE TABLE IF NOT EXISTS NhanSu (
    cccd TEXT PRIMARY KEY,
    ten TEXT,
    ngaysinh TEXT,
    gioitinh TEXT,
    diachi TEXT
)
""")
conn.commit()


# ===== Thêm nhân sự =====
def them_nhan_su():
    cccd = input("Nhap CCCD: ")
    ten = input("Nhap ten: ")
    ngaysinh = input("Nhap ngay sinh: ")
    gioitinh = input("Nhap gioi tinh: ")
    diachi = input("Nhap dia chi: ")

    try:
        cursor.execute("INSERT INTO NhanSu VALUES (?, ?, ?, ?, ?)",
                       (cccd, ten, ngaysinh, gioitinh, diachi))
        conn.commit()
        print("Them thanh cong!")
    except:
        print("CCCD da ton tai!")


# ===== Hiển thị =====
def hien_thi():
    cursor.execute("SELECT * FROM NhanSu")
    ds = cursor.fetchall()

    print("\nDanh sach nhan su:")
    for row in ds:
        print(row)


# ===== Sửa =====
def sua_nhan_su():
    cccd = input("Nhap CCCD can sua: ")

    ten = input("Nhap ten moi: ")
    ngaysinh = input("Nhap ngay sinh moi: ")
    gioitinh = input("Nhap gioi tinh moi: ")
    diachi = input("Nhap dia chi moi: ")

    cursor.execute("""
    UPDATE NhanSu
    SET ten=?, ngaysinh=?, gioitinh=?, diachi=?
    WHERE cccd=?
    """, (ten, ngaysinh, gioitinh, diachi, cccd))

    conn.commit()
    print("Cap nhat thanh cong!")


# ===== Xóa =====
def xoa_nhan_su():
    cccd = input("Nhap CCCD can xoa: ")

    cursor.execute("DELETE FROM NhanSu WHERE cccd=?", (cccd,))
    conn.commit()

    print("Xoa thanh cong!")


# ===== Tìm kiếm =====
def tim_kiem():
    tu_khoa = input("Nhap CCCD/ten/dia chi can tim: ")

    cursor.execute("""
    SELECT * FROM NhanSu
    WHERE cccd LIKE ? OR ten LIKE ? OR diachi LIKE ?
    """, ('%' + tu_khoa + '%',
          '%' + tu_khoa + '%',
          '%' + tu_khoa + '%'))

    ket_qua = cursor.fetchall()

    print("Ket qua tim kiem:")
    for row in ket_qua:
        print(row)


# ===== Menu =====
while True:
    print("\n===== MENU =====")
    print("1. Them nhan su")
    print("2. Hien thi danh sach")
    print("3. Sua nhan su")
    print("4. Xoa nhan su")
    print("5. Tim kiem")
    print("0. Thoat")

    chon = input("Nhap lua chon: ")

    if chon == "1":
        them_nhan_su()
    elif chon == "2":
        hien_thi()
    elif chon == "3":
        sua_nhan_su()
    elif chon == "4":
        xoa_nhan_su()
    elif chon == "5":
        tim_kiem()
    elif chon == "0":
        break
    else:
        print("Lua chon khong hop le!")

# Đóng kết nối
conn.close()