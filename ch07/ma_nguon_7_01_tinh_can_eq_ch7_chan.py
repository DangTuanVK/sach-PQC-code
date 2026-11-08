# Mã nguồn 7.1 - Tính cận 7.13 cho tỉ lệ giải mã sai của ba bộ tham số. Chương trình cần NumPy và chạy khoảng một phút.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 7, trang 147
# Trích tự động từ chapters/ch7/main.tex (dòng 1419) bằng extract.py; không sửa tay file này.

import numpy as np
from math import comb, log2
q, n = 3329, 256
def tron(a, b):                   # [a/b], nua len tren
    return (2 * a + b) // (2 * b)
def sai_so_nen(d):                # Decompress(Compress(x)) - x
    pb = {}
    for x in range(q):
        y = tron(2**d * x, q) % 2**d
        e = (tron(q * y, 2**d) - x) % q
        e = e - q if e > q // 2 else e
        pb[e] = pb.get(e, 0) + 1 / q
    return pb
def cbd(eta):                     # nhi thuc tam
    return {i: comb(2*eta, eta+i) / 4**eta for i in range(-eta, eta+1)}
def ket_hop(A, B, phep):          # phan bo cua phep(X, Y)
    C = {}
    for a, pa in A.items():
        for b, pb in B.items():
            v = phep(a, b); C[v] = C.get(v, 0) + pa * pb
    return C
cong = lambda A, B: ket_hop(A, B, lambda a, b: a + b)
nhan = lambda A, B: ket_hop(A, B, lambda a, b: a * b)
def tong_m(A, m):                 # tong m ban sao doc lap
    lo = min(A)
    p = np.array([A.get(v, 0) for v in range(lo, max(A) + 1)])
    kq, lo_kq = np.array([1.0]), 0
    while m:                      # binh phuong lien tiep
        if m & 1:
            kq, lo_kq = np.convolve(kq, p), lo_kq + lo
        p, lo, m = np.convolve(p, p), 2 * lo, m >> 1
    return {lo_kq + i: x for i, x in enumerate(kq)}
def dfr(k, eta1, eta2, du, dv):
    ey = tong_m(nhan(cbd(eta1), cbd(eta1)), k * n)
    se = tong_m(nhan(cbd(eta1),
                     cong(cbd(eta2), sai_so_nen(du))), k * n)
    F = cong(cong(ey, se), cong(cbd(eta2), sai_so_nen(dv)))
    duoi = sum(p for v, p in F.items() if abs(v) >= 832)
    return log2(n * duoi)         # chan hop tren 256 he so
for ten, ts in [("512", (2, 3, 2, 10, 4)), ("768", (3, 2, 2, 10, 4)),
                ("1024", (4, 2, 2, 11, 5))]:
    print(f"ML-KEM-{ten}: delta <= 2^{dfr(*ts):.2f}")
