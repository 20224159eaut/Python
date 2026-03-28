from datetime import datetime
nam_sinh = int(input("Nhập năm sinh: "))
nam_hien_tai = datetime.now().year

if nam_sinh <= 0 or nam_sinh > nam_hien_tai:
    print("Năm sinh không hợp lệ")
else:
    tuoi = nam_hien_tai - nam_sinh

    can_list = ["Canh", "Tân", "Nhâm", "Quý", "Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ"]
    can = can_list[nam_sinh % 10]

    chi_list = ["Khỉ", "Dậu", "Tuất", "Hợi", "Tý", "Trẩu", "Hổ", "Mão", "Rồng", "Chuột", "Ngựa", "Mùi"]
    chi = chi_list[nam_sinh % 12]

    menh_list = ["Kim", "Thủy", "Lửa", "Thổ", "Mộc"]
    menh = menh_list[nam_sinh % 5]

    print("Sinh năm {0} thuộc {1} {2}, mệnh {3}, vậy bạn {4} tuổi".format(
        nam_sinh, can, chi, menh, tuoi
    ))
    