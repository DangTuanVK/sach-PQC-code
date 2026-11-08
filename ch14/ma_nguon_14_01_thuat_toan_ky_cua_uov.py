# Mã nguồn 14.1 - Thuật toán ký của UOV. Toàn bộ độ khó nằm ở việc đối thủ không biết không gian dầu T^-1(O); khi biết nó, việc ký chỉ còn là khử Gauss.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 14, trang 305
# Trích tự động từ chapters/ch14/main.tex (dòng 1056) bằng extract.py; không sửa tay file này.

def sign(self, y, so_lan=200):
    """Chon ngau nhien bien giam, giai he TUYEN TINH theo bien dau."""
    F, n, m, v = self.F, self.n, self.m, self.v
    for _ in range(so_lan):
        xv = [self.rng.randrange(F.n) for _ in range(v)]   # co dinh giam
        A = [[0]*(m+1) for _ in range(m)]
        for e, Q in enumerate(self.Fc):
            hs = 0
            for i in range(v):                    # phan giam-giam: hang so
                for j in range(i, v):
                    if Q[i][j]:
                        hs ^= F.mul(Q[i][j], F.mul(xv[i], xv[j]))
            A[e][m] = hs ^ y[e]
            for k in range(m):                    # phan giam-dau: tuyen tinh
                c = 0
                for i in range(v):
                    if Q[i][v+k]:
                        c ^= F.mul(Q[i][v+k], xv[i])
                A[e][k] = c
        xo = self._giai(A, m)                     # khu Gauss
        if xo is None:
            continue                              # he suy bien, thu lai
        return self._nhan(self.Ti, xv + xo)       # doi bien nguoc
    return None
