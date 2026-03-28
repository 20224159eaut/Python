n = int(input("Nhap so nguyen duong: "))

if n % 2 == 0 and n % 3 == 0:
    print("So chia het cho ca 2 va 3")
elif n % 2 == 0:
    print("So chia het cho 2")
elif n % 3 == 0:
    print("So chia het cho 3")
else:
    print("So khong chia het cho 2 va 3")
    