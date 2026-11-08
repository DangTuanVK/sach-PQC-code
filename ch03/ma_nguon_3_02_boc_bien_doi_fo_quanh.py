# Mã nguồn 3.2 - Bọc biến đổi FO quanh hệ mã hóa của Mã nguồn 3.1, mô phỏng cấu trúc của Thuật toán 17 và 18 trong FIPS 203. Hàm G là SHA3-512, hàm H là SHA3-256 (dùng thay cho J), bam_ct băm bản mã.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 3, trang 36
# Trích tự động từ chapters/ch3/main.tex (dòng 531) bằng extract.py; không sửa tay file này.

def encaps(pk, h, rng):                            # h = H(pk), tinh mot lan
    m = rng.randint(0, 1)                          # |M| = 2: CHI DE MINH HOA
    K_r = G(bytes([m]), h)                         # (K, r) <- G(m || h)
    K, r_seed = K_r[:32], int.from_bytes(K_r[32:], "big")
    ct = encrypt(pk, m, random.Random(r_seed))     # ngau nhien DAN XUAT tu m
    return ct, K

def decaps(pk, h, sk, z, ct):
    m2 = decrypt(sk, ct)
    K_r = G(bytes([m2]), h)
    K2, r_seed = K_r[:32], int.from_bytes(K_r[32:], "big")
    ct2 = encrypt(pk, m2, random.Random(r_seed))   # MA HOA LAI
    if ct != ct2:
        return H(z, bam_ct(ct))                    # tu choi ngam: J(z || c)
    return K2
