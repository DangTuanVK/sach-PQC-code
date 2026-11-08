# Mã nguồn 6.3 - Phép nhân trực tiếp trong Z_q[X]/(X^256+1), dùng làm chuẩn đối chiếu cho NTT.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 6, trang 120
# Trích tự động từ chapters/ch6/main.tex (dòng 2361) bằng extract.py; không sửa tay file này.

def nhan_truc_tiep(f, g, q):
    """Nhan trong Z_q[X]/(X^256+1) theo dinh nghia -- O(n^2)."""
    h = [0]*256
    for i in range(256):
        if not f[i]:
            continue
        for j in range(256):
            k = i + j
            if k < 256:
                h[k] = (h[k] + f[i]*g[j]) % q
            else:
                h[k-256] = (h[k-256] - f[i]*g[j]) % q   # X^256 = -1
    return h
