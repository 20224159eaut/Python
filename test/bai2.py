class BaiTapChuoi:
    def __init__(self, s1, s2, s3):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3

    def toan_so_sanh(self):
        print("=== TOÁN SO SÁNH ===")
        print("s1 > s2:", self.s1 > self.s2)
        print("s1 < s2:", self.s1 < self.s2)
        print("s1 == s2:", self.s1 == self.s2)
        print("s1 != s2:", self.s1 != self.s2)
        print("s2 >= s3:", self.s2 >= self.s3)
        print("s2 <= s3:", self.s2 <= self.s3)

    def toan_logic(self):
        print("\n=== TOÁN LOGIC ===")
        print("(s1 < s2) and (s2 < s3):", (self.s1 < self.s2) and (self.s2 < self.s3))
        print("(s1 > s2) or (s2 < s3):", (self.s1 > self.s2) or (self.s2 < self.s3))
        print("not(s1 < s2):", not (self.s1 < self.s2))


# Chạy chương trình
obj = BaiTapChuoi('a', 'b', 'c')

obj.toan_so_sanh()
obj.toan_logic()