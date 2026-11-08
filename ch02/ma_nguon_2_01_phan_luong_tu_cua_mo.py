# Mã nguồn 2.1 - Phần lượng tử của mô phỏng Shor: chọn q, dựng phổ sau QFT và lấy mẫu kết quả đo.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 2, trang 21
# Trích tự động từ chapters/ch2/main.tex (dòng 408) bằng extract.py; không sửa tay file này.

import cmath, random
from fractions import Fraction; from math import gcd

def chon_q(N):
    """q la luy thua cua 2 nho nhat thoa N^2 <= q < 2N^2 (Shor 1997)."""
    t = (N * N - 1).bit_length()
    return 1 << t, t

def pho_sau_qft(N, x, y=None, rng=random):
    """Tra ve (q, t, y, tap a, pho xac suat khi do thanh ghi 1)."""
    q, t = chon_q(N)
    f = [pow(x, a, N) for a in range(q)]
    if y is None:
        y = f[rng.randrange(q)]                  # do thanh ghi 2
    tap_a = [a for a in range(q) if f[a] == y]   # cap so cong cong sai r
    chuan = 1.0 / (q * len(tap_a))**0.5
    pho = []
    for c in range(q):                           # QFT theo dinh nghia
        bien_do = sum(cmath.exp(2j*cmath.pi*c*a/q) for a in tap_a) * chuan
        pho.append(abs(bien_do)**2)
    return q, t, y, tap_a, pho

def do(pho, rng):                                # lay mau c theo pho xac suat
    return rng.choices(range(len(pho)), weights=pho)[0]
