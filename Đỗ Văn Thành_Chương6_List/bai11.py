n = int(input("Nhap n: "))
_list = ['apple', 'banana', 'cat', 'dog', 'elephant']
ket_qua = []
for tu in _list:
    if len(tu) > n:
        ket_qua.append(tu)
print("Cac tu co do dai > n:", ket_qua)