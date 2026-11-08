# Mã nguồn 3.2b - (khối mã không đánh số, sau Mã nguồn 3.2)
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 3, trang 36
# Trích tự động từ chapters/ch3/main.tex (dòng 560) bằng extract.py; không sửa tay file này.

def nghe_len(pk, h, ct):
    for m in (0, 1):                               # thu het khong gian M
        K_r = G(bytes([m]), h)
        r_seed = int.from_bytes(K_r[32:], "big")
        if encrypt(pk, m, random.Random(r_seed)) == ct:
            return K_r[:32]
