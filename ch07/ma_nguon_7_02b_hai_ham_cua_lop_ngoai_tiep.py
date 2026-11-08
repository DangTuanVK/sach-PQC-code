# Mã nguồn 7.2b - (khối mã không đánh số, sau Mã nguồn 7.2)
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 7, trang 149
# Trích tự động từ chapters/ch7/main.tex (dòng 1599) bằng extract.py; không sửa tay file này.

def sample_ntt(seed32, j, i):
    """Thuat toan 7: lay mau tu choi tu SHAKE128."""
    buf = shake_128(seed32 + bytes([j, i])).digest(3*800)
    a, p = [], 0
    while len(a) < 256:
        C0, C1, C2 = buf[p], buf[p+1], buf[p+2]; p += 3
        d1 = C0 + 256*(C1 % 16)          # 0 <= d1 < 2^12
        d2 = (C1 >> 4) + 16*C2           # 0 <= d2 < 2^12
        if d1 < q:
            a.append(d1)
        if d2 < q and len(a) < 256:
            a.append(d2)
    return a
