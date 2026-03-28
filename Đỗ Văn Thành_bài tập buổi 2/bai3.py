# Nhập 3 số nguyên
a = int(input("Nhập số a: "))
b = int(input("Nhập số b: "))
c = int(input("Nhập số c: "))

# a. Tổng và tích
tong = a + b + c
tich = a * b * c

print("=== a. Tổng và tích ===")
print("Tổng =", tong)
print("Tích =", tich)

# b. Hiệu của các cặp số
print("\n=== b. Hiệu của các cặp ===")
print("a - b =", a - b)
print("a - c =", a - c)
print("b - c =", b - c)

# c. Chia 2 số (ví dụ chọn a và b)
print("\n=== c. Phép chia a và b ===")

if b != 0:
    print("Chia nguyên (a // b):", a // b)
    print("Chia dư (a % b):", a % b)
    print("Chia chính xác (a / b):", a / b)
else:
    print("Không thể chia cho 0")