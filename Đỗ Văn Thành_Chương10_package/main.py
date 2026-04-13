# Import từ package math_utils
from math_utils import cong_phan_so, dien_tich_hcn

def main():
    print("--- Chào mừng đến với Math Utils ---")
    
    # 1. Thử nghiệm phân số: (1/2) + (1/3)
    p1 = (1, 2)
    p2 = (1, 3)
    kq_ps = cong_phan_so(p1, p2)
    print(f"Tổng phân số {p1} + {p2} = {kq_ps[0]}/{kq_ps[1]}")
    
    # 2. Thử nghiệm hình học: Diện tích HCN 5x10
    dai, rong = 5, 10
    kq_hh = dien_tich_hcn(dai, rong)
    print(f"Diện tích hình chữ nhật ({dai}x{rong}) = {kq_hh}")

if __name__ == "__main__":
    main()