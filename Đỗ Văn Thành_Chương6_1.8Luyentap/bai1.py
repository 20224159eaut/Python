bang_ma = {'a': '!', 'b': '@', 'c': '#', 'd': '$'}

bang_giai_ma = {}

for k, v in bang_ma.items():
    bang_giai_ma[v] = k

chuoi = input("Nhap chuoi: ")

ma_hoa = ""

for ky_tu in chuoi:
    if ky_tu in bang_ma:
        ma_hoa = ma_hoa + bang_ma[ky_tu]
    else:
        ma_hoa = ma_hoa + ky_tu

print("Chuoi ma hoa:", ma_hoa)

giai_ma = ""

for ky_tu in ma_hoa:
    if ky_tu in bang_giai_ma:
        giai_ma = giai_ma + bang_giai_ma[ky_tu]
    else:
        giai_ma = giai_ma + ky_tu

print("Chuoi giai ma:", giai_ma)