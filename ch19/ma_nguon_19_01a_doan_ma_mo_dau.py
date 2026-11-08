# Mã nguồn 19.1a - (khối mã không đánh số, đứng trước Mã nguồn 19.1)
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 19, trang 370
# Trích tự động từ chapters/ch20/main.tex (dòng 228) bằng extract.py; không sửa tay file này.

import random
n, q, t = 64, 1 << 40, 256          # bac, modulus ban ma, modulus ban ro
D = q // t                          # he so ti le Delta

def modq(f):     return [x % q for x in f]
def modpm(x):                       # dai dien tam trong (-q/2, q/2]
    x %= q
    return x - q if x > q // 2 else x
def cong(f, g):  return [(x + y) % q for x, y in zip(f, g)]
def nhan_chinh_xac(f, g):           # nhan trong Z[X]/(X^n+1), KHONG rut gon
    h = [0] * n
    for i in range(n):
        for j in range(n):
            if i + j < n: h[i + j] += f[i] * g[j]
            else:         h[i + j - n] -= f[i] * g[j]      # X^n = -1
    return h
def nhan(f, g):       return modq(nhan_chinh_xac(f, g))
def nhi_phan(rng):    return [rng.randrange(2) for _ in range(n)]
def ngau_nhien(rng):  return [rng.randrange(q) for _ in range(n)]
def nhieu_nho(rng):   return [rng.randrange(2) + rng.randrange(2)
                              - rng.randrange(2) - rng.randrange(2)
                              for _ in range(n)]           # nhi thuc tam, eta=2
