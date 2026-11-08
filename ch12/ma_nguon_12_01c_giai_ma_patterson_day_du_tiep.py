# Mã nguồn 12.1c - (khối mã không đánh số, sau Mã nguồn 12.1)
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 12, trang 273
# Trích tự động từ chapters/ch12/main.tex (dòng 369) bằng extract.py; không sửa tay file này.

def prange(T, s, n, mt, t, rng, gioi_han=200000):
    """Doan mt cot chua loi, giai he tuyen tinh, kiem trong so."""
    H = [[1 if i == j else 0 for j in range(mt)] + T[i][:] for i in range(mt)]
    thu = 0
    while thu < gioi_han:
        thu += 1
        cot = rng.sample(range(n), mt)              # phan bu tap thong tin
        M = [[H[i][c] for c in cot] + [s[i]] for i in range(mt)]
        R, tru = rref(M, mt)
        if len(tru) < mt:
            continue                                 # khong kha nghich
        e = [0]*n
        for r, c in enumerate(tru):
            if R[r][mt]:
                e[cot[c]] = 1
        if sum(e) <= t and kiem_hoi_chung(H, e) == s:
            return e, thu
    return None, thu
