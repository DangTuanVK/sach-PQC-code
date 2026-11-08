# Mã nguồn 5.1b - (khối mã không đánh số, sau Mã nguồn 5.1)
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 5, trang 78
# Trích tự động từ chapters/ch5/main.tex (dòng 1717) bằng extract.py; không sửa tay file này.

def pha_lwe(A, b, n, m, q):
    """Nhung Kannan: vector (-e, s, -1) nam trong luoi va rat ngan."""
    d = m + n + 1
    B = [[q if k == i else 0 for k in range(d)] for i in range(m)]
    for j in range(n):
        B.append([A[i][j] for i in range(m)] +
                 [1 if k == j else 0 for k in range(n)] + [0])
    B.append(list(b) + [0]*n + [1])
    for v in lll(B):
        if v[-1] in (1, -1):
            dau = -v[-1]
            s = [dau*v[m+j] for j in range(n)]
            if all(abs(x) <= 1 for x in s):
                return s
    return None
