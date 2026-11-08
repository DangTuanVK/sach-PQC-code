# Không có trong sách: so hoc F_16, sinh khoa UOV (P = F o T), giai he tuyen tinh, xac minh; dung lai ham ky cua Ma nguon 14.1. Tái tạo kết quả in sau Mã nguồn 13.1 (chapters/ch14/main.tex).
"""Module phu tro cho UOV thu nho tren F_16 (Chuong 14).

Sach chi in ham ky (Ma nguon 14.1). Tep nay bo sung truong F_16, sinh khoa theo
cach nhin co dien P = F o T (anh xa trung tam F khong co so hang dau-dau, ma
tran doi bien T kha nghich), khu Gauss _giai, nhan ma tran _nhan va xac minh.
Ham ky cua sach duoc gan nguyen van vao lop UOV.
"""
import contextlib as _ctx
import io as _io

with _ctx.redirect_stdout(_io.StringIO()):
    import ma_nguon_13_01_thuat_toan_ky_cua_uov as _mn


class GF16:
    """F_16 = F_2[x]/(x^4 + x + 1), phan tu la so nguyen 0..15."""

    def __init__(self):
        self.m, self.n = 4, 16
        self.exp = [0] * 30
        self.log = [0] * 16
        x = 1
        for i in range(15):
            self.exp[i] = self.exp[i + 15] = x
            self.log[x] = i
            x <<= 1
            if x & 0x10:
                x ^= 0b10011
        self._mul = [[self._mul_log(a, b) for b in range(16)] for a in range(16)]

    def _mul_log(self, a, b):
        if a == 0 or b == 0:
            return 0
        return self.exp[self.log[a] + self.log[b]]

    def mul(self, a, b):
        return self._mul[a][b]

    def inv(self, a):
        if a == 0:
            raise ZeroDivisionError("nghich dao cua 0")
        return self.exp[15 - self.log[a]]


class UOV:
    sign = _mn.sign                           # Ma nguon 14.1

    def __init__(self, n, m, rng):
        self.F, self.n, self.m, self.v, self.rng = GF16(), n, m, n - m, rng
        self.keygen()

    # ---- dai so tuyen tinh tren F_16 ----
    def _giai(self, A, so_an):
        """Khu Gauss tren ma tran mo rong so_an x (so_an+1); None neu suy bien."""
        F = self.F
        A = [row[:] for row in A]
        for c in range(so_an):
            p = next((i for i in range(c, so_an) if A[i][c]), None)
            if p is None:
                return None
            A[c], A[p] = A[p], A[c]
            iv = F.inv(A[c][c])
            A[c] = [F.mul(iv, x) for x in A[c]]
            for i in range(so_an):
                if i != c and A[i][c]:
                    f = A[i][c]
                    A[i] = [x ^ F.mul(f, y) for x, y in zip(A[i], A[c])]
        return [A[i][so_an] for i in range(so_an)]

    def _nhan(self, M, x):
        F = self.F
        kq = []
        for row in M:
            s = 0
            for a, b in zip(row, x):
                if a and b:
                    s ^= F.mul(a, b)
            kq.append(s)
        return kq

    def _nghich_dao(self, M):
        """Nghich dao ma tran n x n; None neu suy bien."""
        F, n = self.F, len(M)
        A = [M[i][:] + [1 if i == j else 0 for j in range(n)] for i in range(n)]
        for c in range(n):
            p = next((i for i in range(c, n) if A[i][c]), None)
            if p is None:
                return None
            A[c], A[p] = A[p], A[c]
            iv = F.inv(A[c][c])
            A[c] = [F.mul(iv, x) for x in A[c]]
            for i in range(n):
                if i != c and A[i][c]:
                    f = A[i][c]
                    A[i] = [x ^ F.mul(f, y) for x, y in zip(A[i], A[c])]
        return [row[n:] for row in A]

    # ---- sinh khoa ----
    def keygen(self):
        F, n, m, v, rng = self.F, self.n, self.m, self.v, self.rng
        # Anh xa trung tam: Q tam giac tren, khoi dau-dau (i, j >= v) bang 0
        self.Fc = []
        for _ in range(m):
            Q = [[0] * n for _ in range(n)]
            for i in range(v):
                for j in range(i, n):
                    Q[i][j] = rng.randrange(F.n)
            self.Fc.append(Q)
        while True:
            T = [[rng.randrange(F.n) for _ in range(n)] for _ in range(n)]
            Ti = self._nghich_dao(T)
            if Ti is not None:
                break
        self.T, self.Ti = T, Ti
        # Khoa cong khai: P_e(x) = F_e(T x), luu dang tam giac tren cua T^t Q T
        self.P = []
        for Q in self.Fc:
            QT = [[0] * n for _ in range(n)]               # Q T
            for i in range(n):
                for j in range(n):
                    s = 0
                    for k in range(n):
                        if Q[i][k] and T[k][j]:
                            s ^= F.mul(Q[i][k], T[k][j])
                    QT[i][j] = s
            M = [[0] * n for _ in range(n)]                # T^t (Q T)
            for i in range(n):
                for j in range(n):
                    s = 0
                    for k in range(n):
                        if T[k][i] and QT[k][j]:
                            s ^= F.mul(T[k][i], QT[k][j])
                    M[i][j] = s
            P = [[0] * n for _ in range(n)]
            for i in range(n):
                P[i][i] = M[i][i]
                for j in range(i + 1, n):
                    P[i][j] = M[i][j] ^ M[j][i]
            self.P.append(P)

    def so_he_so_pk(self):
        return sum(1 for P in self.P for i in range(self.n) for j in range(i, self.n))

    def verify(self, x, y):
        """Kiem P(x) = y bang khoa cong khai."""
        F, n = self.F, self.n
        if x is None:
            return False
        for e, P in enumerate(self.P):
            s = 0
            for i in range(n):
                if x[i] == 0:
                    continue
                for j in range(i, n):
                    if P[i][j] and x[j]:
                        s ^= F.mul(P[i][j], F.mul(x[i], x[j]))
            if s != y[e]:
                return False
        return True
