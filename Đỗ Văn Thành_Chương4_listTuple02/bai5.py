# ===== BAI 5 =====

# Doc file
f = open("demo_file2.txt", "r", encoding="utf-8")
noi_dung = f.read()
f.close()

# Tach tu -> list
ds_tu = noi_dung.split()

# Dem so lan xuat hien
ket_qua = {}

for tu in ds_tu:
    if tu in ket_qua:
        ket_qua[tu] += 1
    else:
        ket_qua[tu] = 1

# Chuyen sang tuple de in (khong bat buoc, de dung tuple)
ket_qua_tuple = tuple(ket_qua.items())

# In ket qua
print("Ket qua:")
for x in ket_qua_tuple:
    print(x[0], ":", x[1])
    