# Mã nguồn 9.1 - Bộ lấy mẫu Gauss rời rạc bằng bảng CDT. Vòng lặp trong lay_mau_ct luôn chạy đủ 2T+1 bước bất kể giá trị lấy được.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 9, trang 215
# Trích tự động từ chapters/ch9/main.tex (dòng 934) bằng extract.py; không sửa tay file này.

import math, secrets

SIGMA, T, BIT = 1.8205, 12, 63          # sigma_max cua Falcon

def ly_thuyet(sigma=SIGMA, t=T):
    w = {x: math.exp(-x*x / (2*sigma*sigma)) for x in range(-t, t+1)}
    tong = sum(w.values())
    return {x: w[x]/tong for x in w}

def bang_cdt(sigma=SIGMA, t=T, bit=BIT):
    """Bang phan phoi tich luy, thang len 2^bit de tra cuu bang so nguyen."""
    lt, cdt, acc = ly_thuyet(sigma, t), [], 0.0
    for x in range(-t, t+1):
        acc += lt[x]
        cdt.append((min(int(acc * (1 << bit)), (1 << bit) - 1), x))
    return cdt

CDT = bang_cdt()
NGUONG, GIATRI = zip(*CDT)              # nguong tich luy, gia tri tuong ung

def lay_mau_ct(bit=BIT):
    """THOI GIAN HANG: duyet het bang, khong re nhanh, khong thoat som.
       Chi so ket qua = so nguong ma u vuot qua."""
    u = secrets.randbits(bit)
    idx = 0
    for n in NGUONG:
        idx += int(u >= n)          # cong 0 hoac 1, khong re nhanh
    return GIATRI[min(idx, len(GIATRI) - 1)]
