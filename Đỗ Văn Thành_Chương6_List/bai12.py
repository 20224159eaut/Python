n = int(input("Nhap do dai toi thieu: "))

chuoi_nhap = input("Nhap cac chuoi, cach nhau boi dau phay: ")

_list = chuoi_nhap.split(",")

for i in range(len(_list)):
    _list[i] = _list[i].strip()

dem = 0

for s in _list:
    if len(s) >= n and s[0] == s[-1]:
        dem = dem + 1

print("So chuoi thoa man:", dem)