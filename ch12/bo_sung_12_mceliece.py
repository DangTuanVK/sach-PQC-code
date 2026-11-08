# Không có trong sách: so hoc GF(2^m), da thuc tren GF(2^m), lop ma Goppa (sinh khoa, ma hoa, giai ma) dung lai Ma nguon 12.1, 12.1b, 12.1c. Tái tạo kết quả in sau Mã nguồn 12.1 (chapters/ch12/main.tex).
"""Module phu tro cho McEliece thu nho (Chuong 12).

Sach chi in ham giai ma Patterson (Ma nguon 12.1), phep kiem bat kha quy
(khoi 12.1b) va tan cong Prange (khoi 12.1c). Tep nay bo sung phan con thieu:
so hoc GF(2^m) bang bang log, cac ham da thuc p_*, Euclid dung som, sinh khoa
Goppa dang Niederreiter (H he thong (I | T)), ma hoa e -> s = H e va giai ma.
Cac ham phu tro duoc GAN vao module cua sach de ma sach chay nguyen van.
"""
import contextlib as _ctx
import io as _io
import random

with _ctx.redirect_stdout(_io.StringIO()):
    import ma_nguon_12_01_giai_ma_patterson_day_du as _mn1
    import ma_nguon_12_01b_giai_ma_patterson_day_du_tiep as _mn1b
    import ma_nguon_12_01c_giai_ma_patterson_day_du_tiep as _mn1c

# Da thuc nguyen thuy cho GF(2^m) (bit i = he so x^i)
DA_THUC_NGUYEN_THUY = {2: 0b111, 3: 0b1011, 4: 0b10011, 5: 0b100101,
                       6: 0b1000011, 7: 0b10000011, 8: 0b100011101}


class GF2m:
    """Truong GF(2^m), phan tu la so nguyen 0..2^m-1, nhan bang bang log."""

    def __init__(self, m):
        self.m, self.n = m, 1 << m
        poly = DA_THUC_NGUYEN_THUY[m]
        self.exp = [0] * (2 * self.n)
        self.log = [0] * self.n
        x = 1
        for i in range(self.n - 1):
            self.exp[i] = x
            self.log[x] = i
            x <<= 1
            if x & self.n:
                x ^= poly
        for i in range(self.n - 1, 2 * self.n):
            self.exp[i] = self.exp[i - (self.n - 1)]

    def mul(self, a, b):
        if a == 0 or b == 0:
            return 0
        return self.exp[self.log[a] + self.log[b]]

    def inv(self, a):
        if a == 0:
            raise ZeroDivisionError("nghich dao cua 0")
        return self.exp[(self.n - 1) - self.log[a]]


# ---- Da thuc tren GF(2^m): danh sach he so, bac thap truoc; [0] la da thuc 0 ----

def p_norm(a):
    a = list(a)
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    return a or [0]


def p_deg(a):
    a = p_norm(a)
    return -1 if a == [0] else len(a) - 1


def p_add(a, b):
    r = [0] * max(len(a), len(b))
    for i, c in enumerate(a):
        r[i] ^= c
    for i, c in enumerate(b):
        r[i] ^= c
    return p_norm(r)


def p_mul(F, a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    r[i + j] ^= F.mul(x, y)
    return p_norm(r)


def p_divmod(F, a, b):
    a, b = p_norm(a), p_norm(b)
    db = p_deg(b)
    if db < 0:
        raise ZeroDivisionError("chia cho da thuc 0")
    inv_lc = F.inv(b[-1])
    q = [0] * max(1, len(a) - db)
    r = a[:]
    while p_deg(r) >= db:
        d = p_deg(r)
        c = F.mul(r[d], inv_lc)
        q[d - db] = c
        for i, y in enumerate(b):
            r[d - db + i] ^= F.mul(c, y)
        r = p_norm(r)
    return p_norm(q), r


def p_mod(F, a, b):
    return p_divmod(F, a, b)[1]


def p_eval(F, a, x):
    r = 0
    for c in reversed(a):
        r = F.mul(r, x) ^ c
    return r


def p_egcd(F, a, b):
    """Tra ve (d, u, v) voi u a + v b = d, d monic (neu khac 0)."""
    r0, r1 = p_norm(a), p_norm(b)
    u0, u1, v0, v1 = [1], [0], [0], [1]
    while p_deg(r1) >= 0:
        q, r = p_divmod(F, r0, r1)
        r0, r1 = r1, r
        u0, u1 = u1, p_add(u0, p_mul(F, q, u1))
        v0, v1 = v1, p_add(v0, p_mul(F, q, v1))
    if p_deg(r0) >= 0:
        c = [F.inv(r0[-1])]
        r0, u0, v0 = p_mul(F, c, r0), p_mul(F, c, u0), p_mul(F, c, v0)
    return r0, u0, v0


def p_inv_mod(F, a, g):
    d, u, _ = p_egcd(F, a, g)
    if p_deg(d) != 0:
        raise ValueError("khong kha nghich theo modulo g")
    return p_mod(F, u, g)


def p_sqrt_mod(F, a, g):
    """sqrt(a) = a^(2^(m t - 1)) mod g, dung khi g bat kha quy (eq:ch12-sqrt)."""
    r = p_mod(F, a, g)
    for _ in range(F.m * p_deg(g) - 1):
        r = p_mod(F, p_mul(F, r, r), g)
    return r


def _eea_dung_som(self, R, g, nguong):
    """Euclid mo rong tren (g, R), dung khi bac phan du <= nguong = t//2.
    Tra ve (a, b) voi a = b R (mod g)."""
    F = self.F
    r0, r1 = g, p_mod(F, R, g)
    b0, b1 = [0], [1]
    while p_deg(r1) > nguong:
        q, r = p_divmod(F, r0, r1)
        r0, r1 = r1, r
        b0, b1 = b1, p_add(b0, p_mul(F, q, b1))
    return r1, b1


# ---- Dai so tuyen tinh tren GF(2) cho Prange ----

def rref(M, so_cot):
    """Dua ma tran nhi phan ve dang bac thang rut gon tren so_cot cot dau.
    Tra ve (R, tru) voi tru[r] la cot tru cua hang r."""
    R = [row[:] for row in M]
    tru, h = [], 0
    for c in range(so_cot):
        p = next((i for i in range(h, len(R)) if R[i][c]), None)
        if p is None:
            continue
        R[h], R[p] = R[p], R[h]
        for i in range(len(R)):
            if i != h and R[i][c]:
                R[i] = [x ^ y for x, y in zip(R[i], R[h])]
        tru.append(c)
        h += 1
    return R, tru


def kiem_hoi_chung(H, e):
    return [sum(h & x for h, x in zip(row, e)) & 1 for row in H]


# Gan cac ham phu tro vao module cua sach
for _mod in (_mn1, _mn1b, _mn1c):
    for _ten in ("p_add", "p_mul", "p_mod", "p_eval", "p_deg", "p_egcd",
                 "p_inv_mod", "p_sqrt_mod", "rref", "kiem_hoi_chung"):
        setattr(_mod, _ten, globals()[_ten])

prange = _mn1c.prange


class Goppa:
    """McEliece thu nho dang Niederreiter (nhu Classic McEliece)."""

    patterson = _mn1.patterson              # Ma nguon 12.1
    _bat_kha_quy = _mn1b._bat_kha_quy       # khoi 12.1b
    _eea_dung_som = _eea_dung_som

    def __init__(self, m, t, n, rng):
        self.F, self.m, self.t, self.n, self.rng = GF2m(m), m, t, n, rng
        self.keygen()

    def keygen(self):
        F, m, t, n = self.F, self.m, self.t, self.n
        while True:
            g = [self.rng.randrange(F.n) for _ in range(t)] + [1]   # monic bac t
            if not self._bat_kha_quy(g):
                continue
            L = self.rng.sample(range(F.n), n)
            # Ma tran kiem tra nhi phan: cot j la he so cua (z - a_j)^-1 mod g
            H = [[0] * n for _ in range(m * t)]
            for j, a in enumerate(L):
                h = p_inv_mod(F, p_add([a], [0, 1]), g)
                h = h + [0] * (t - len(h))
                for i in range(t):
                    for b in range(m):
                        H[i * m + b][j] = (h[i] >> b) & 1
            R, tru = rref(H, n)
            if tru != list(range(m * t)):
                continue                       # khong dua duoc ve (I | T): sinh lai
            self.g, self.L = g, L
            self.k = n - m * t
            self.T = [row[m * t:] for row in R]   # khoa cong khai
            self.H = R                            # (I | T)
            return

    def kich_thuoc_pk(self):
        return self.m * self.t * self.k // 8      # floor(mtk/8), khong dem hang

    def ma_hoa(self):
        e = [0] * self.n
        for j in self.rng.sample(range(self.n), self.t):
            e[j] = 1
        return e, kiem_hoi_chung(self.H, e)

    def giai_ma(self, s):
        v = s + [0] * self.k                       # H (s | 0) = s
        e = self.patterson(v)
        if kiem_hoi_chung(self.H, e) != s or sum(e) != self.t:
            return None
        return e
