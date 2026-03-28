class BaiTapToanTu:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def toan_so_hoc(self):
        print("=== TOÁN SỐ HỌC ===")
        print("a + b + c =", self.a + self.b + self.c)
        print("a - b - c =", self.a - self.b - self.c)
        print("a * b * c =", self.a * self.b * self.c)
        print("a / b =", self.a / self.b)
        print("a ** b =", self.a ** self.b)

    def toan_so_sanh(self):
        print("\n=== TOÁN SO SÁNH ===")
        print("a > b:", self.a > self.b)
        print("a < b:", self.a < self.b)
        print("a == b:", self.a == self.b)
        print("a != b:", self.a != self.b)
        print("b >= c:", self.b >= self.c)
        print("b <= c:", self.b <= self.c)

    def toan_gan(self):
        print("\n=== TOÁN GÁN ===")
        x = self.a
        print("Giá trị ban đầu x =", x)

        x += self.b
        print("x += b:", x)

        x -= self.c
        print("x -= c:", x)

        x *= self.b
        print("x *= b:", x)

        x /= self.c
        print("x /= c:", x)

    def toan_logic(self):
        print("\n=== TOÁN LOGIC ===")
        print("(a > b) and (b > c):", (self.a > self.b) and (self.b > self.c))
        print("(a > b) or (b < c):", (self.a > self.b) or (self.b < self.c))
        print("not(a > b):", not (self.a > self.b))

    def toan_bit(self):
        print("\n=== TOÁN BIT ===")
        print("a & b:", self.a & self.b)
        print("a | b:", self.a | self.b)
        print("~a:", ~self.a)
        print("a ^ b:", self.a ^ self.b)
        print("a << 3:", self.a << 3)
        print("a >> 2:", self.a >> 2)


# Chạy chương trình
obj = BaiTapToanTu(16, 3, 5)

obj.toan_so_hoc()
obj.toan_so_sanh()
obj.toan_gan()
obj.toan_logic()
obj.toan_bit()