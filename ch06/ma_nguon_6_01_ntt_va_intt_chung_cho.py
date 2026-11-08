# Mã nguồn 6.1 - NTT và INTT chung cho ML-KEM và ML-DSA. Cùng một hàm: khi gọi với KEM, hàm trùng Thuật toán 9, 10 của FIPS 203; khi gọi với DSA, hàm trùng Thuật toán 41, 42 của FIPS 204.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 6, trang 119
# Trích tự động từ chapters/ch6/main.tex (dòng 2276) bằng extract.py; không sửa tay file này.

KEM = dict(q=3329,    zeta=17,   b=7, L=2, c=3303)      # FIPS 203
DSA = dict(q=8380417, zeta=1753, b=8, L=1, c=8347681)   # FIPS 204

def bitrev(k, b):
    return int(format(k, "0%db" % b)[::-1], 2)

for P in (KEM, DSA):                                    # bang he so xoay
    P["Z"] = [pow(P["zeta"], bitrev(k, P["b"]), P["q"])
              for k in range(2**P["b"])]

def ntt(f, P):
    """Thuat toan 6.2 (FIPS 203 TT 9, FIPS 204 TT 41)."""
    q, Z, f = P["q"], P["Z"], list(f)
    k, length = 1, 128
    while length >= P["L"]:
        for start in range(0, 256, 2*length):
            z = Z[k]; k += 1
            for j in range(start, start + length):
                t = z * f[j + length] % q
                f[j + length] = (f[j] - t) % q
                f[j]          = (f[j] + t) % q
        length //= 2
    return f

def intt(f, P):
    """Thuat toan 6.3 (FIPS 203 TT 10, FIPS 204 TT 42)."""
    q, Z, f = P["q"], P["Z"], list(f)
    k, length = 2**P["b"] - 1, P["L"]
    while length <= 128:
        for start in range(0, 256, 2*length):
            z = Z[k]; k -= 1
            for j in range(start, start + length):
                t = f[j]
                f[j]          = (t + f[j + length]) % q
                f[j + length] = z * (f[j + length] - t) % q
        length *= 2
    return [P["c"] * x % q for x in f]
