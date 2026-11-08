# Mã nguồn 5.1 - Thuật toán LLL. Cơ sở luôn giữ hệ số nguyên; chỉ phần trực giao hóa dùng số thực.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 5, trang 78
# Trích tự động từ chapters/ch5/main.tex (dòng 1655) bằng extract.py; không sửa tay file này.

def lll(B, delta=0.99):
    B = [list(map(int, r)) for r in B]
    n, d = len(B), len(B[0])
    Bs, mu, ns = gso(B)
    k = 1
    while k < n:
        for j in range(k-1, -1, -1):                 # rut gon kich thuoc
            if abs(mu[k][j]) > 0.5:
                r = round(mu[k][j])
                for i in range(d):
                    B[k][i] -= r*B[j][i]
                for i in range(j):
                    mu[k][i] -= r*mu[j][i]
                mu[k][j] -= r
        if ns[k] >= (delta - mu[k][k-1]**2)*ns[k-1]:   # dieu kien Lovasz
            k += 1
        else:
            B[k], B[k-1] = B[k-1], B[k]
            Bs, mu, ns = gso(B)                      # chi tinh lai khi hoan doi
            k = max(k-1, 1)
    return B
