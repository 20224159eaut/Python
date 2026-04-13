def cong_phan_so(p1, p2):
    tu = p1[0] * p2[1] + p2[0] * p1[1]
    mau = p1[1] * p2[1]
    return (tu, mau)

def tru_phan_so(p1, p2):
    tu = p1[0] * p2[1] - p2[0] * p1[1]
    mau = p1[1] * p2[1]
    return (tu, mau)

# Bạn có thể thêm nhân, chia tương tự