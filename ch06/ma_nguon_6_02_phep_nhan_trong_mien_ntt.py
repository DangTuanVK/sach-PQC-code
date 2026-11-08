# Mã nguồn 6.2 - Phép nhân trong miền NTT của hai chuẩn: 128 phép nhân cơ sở cho ML-KEM, 256 phép nhân từng phần tử cho ML-DSA.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 6, trang 118
# Trích tự động từ chapters/ch6/main.tex (dòng 2332) bằng extract.py; không sửa tay file này.

def multiply_ntts_kem(f, g):
    """FIPS 203 TT 11, 12: 128 phep nhan co so."""
    q, h = KEM["q"], [0]*256
    for i in range(128):
        gamma = pow(KEM["zeta"], 2*bitrev(i, 7) + 1, q)
        a0, a1, b0, b1 = f[2*i], f[2*i+1], g[2*i], g[2*i+1]
        h[2*i]   = (a0*b0 + a1*b1 % q * gamma) % q
        h[2*i+1] = (a0*b1 + a1*b0) % q
    return h

def multiply_ntts_dsa(f, g):
    """NTT day du (ML-DSA): nhan tung phan tu."""
    return [x * y % DSA["q"] for x, y in zip(f, g)]
