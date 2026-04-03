# B2
ten_file = input("Nhap ten file: ")
noi_dung = input("Nhap doan van ban: ")

f = open(ten_file, "w", encoding="utf-8")
f.write(noi_dung)
f.close()

# đọc lại
f = open(ten_file, "r", encoding="utf-8")
data = f.read()
f.close()

print("Noi dung file:")
print(data)