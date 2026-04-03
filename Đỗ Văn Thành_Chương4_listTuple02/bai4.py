# ===== BAI 4 =====

# Nhap thong tin
ten = input("Nhap ten: ")
tuoi = input("Nhap tuoi: ")
email = input("Nhap email: ")
skype = input("Nhap skype: ")
dia_chi = input("Nhap dia chi: ")
noi_lam_viec = input("Nhap noi lam viec: ")

# Luu vao tuple (co dinh du lieu)
thong_tin = (ten, tuoi, email, skype, dia_chi, noi_lam_viec)

# Ghi file
f = open("setInfo.txt", "w", encoding="utf-8")
for x in thong_tin:
    f.write(x + "\n")
f.close()

print("Da luu vao file!")

# Doc file
f = open("setInfo.txt", "r", encoding="utf-8")
ds = f.readlines()   # list
f.close()

# Hien thi
print("\nThong tin da luu:")
for x in ds:
    print(x.strip())