class HocVien:
    def __init__(self, ho_ten, ngay_sinh, email, dien_thoai, dia_chi, lop):
        self.ho_ten = ho_ten
        self.ngay_sinh = ngay_sinh
        self.email = email
        self.dien_thoai = dien_thoai
        self.dia_chi = dia_chi
        self.lop = lop

    def show_info(self):
        print(f"--- Thông tin học viên ---")
        print(f"Họ tên: {self.ho_ten}")
        print(f"Ngày sinh: {self.ngay_sinh}")
        print(f"Email: {self.email}")
        print(f"Điện thoại: {self.dien_thoai}")
        print(f"Địa chỉ: {self.dia_chi}")
        print(f"Lớp: {self.lop}")
        print("-" * 25)

    def change_info(self, dia_chi="Hà Nội", lop="IT12.x"):
        self.dia_chi = dia_chi
        self.lop = lop
        print(f"** Đã cập nhật Địa chỉ thành: {dia_chi} và Lớp thành: {lop} **")

if __name__ == "__main__":
    # Khởi tạo đối tượng hv1
    hv1 = HocVien(
        "Do van Thanh", 
        "24/09/2004", 
        "athanh@gmail.com", 
        "0345666789", 
        "Hà Nội", 
        "IT14.1"
    )
    hv1.show_info()
    hv1.change_info()
    hv1.show_info()
    hv1.change_info("Bắc Ninh", "IT12.5")
    hv1.show_info()