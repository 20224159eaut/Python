# B1
ten_file = input("Nhap ten file: ")
n = int(input("Nhap so dong can doc: "))

f = open(ten_file, "r", encoding="utf-8")

# lưu vào list
ds_dong = []

for i in range(n):
    dong = f.readline()
    if dong == "":
        break
    ds_dong.append(dong.strip())

f.close()

# in ra
print("Noi dung doc duoc:")
for x in ds_dong:
    print(x)