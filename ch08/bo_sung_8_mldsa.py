# Không có trong sách: cac ham phu cua ML-DSA (FIPS 204) ma Ma nguon 8.1 goi toi. Tái tạo kết quả in sau Mã nguồn 8.1 (chapters/ch8/main.tex).
#
# Module nay chi bo sung phan sach mo ta bang ma gia (Muc 8.2: ExpandA, ExpandS,
# ExpandMask, SampleInBall, Power2Round, Decompose, MakeHint/UseHint, cac ham
# dong goi, KeyGen, Verify) va dung lai:
#   - sign_internal cua Ma nguon 8.1 (vong lap ky),
#   - ntt/intt cua Ma nguon 6.1 va multiply_ntts_dsa cua Ma nguon 6.2.
# Cac ham phu duoc gan vao module cua Ma nguon 8.1 de sign_internal goi duoc.
import contextlib as _ctx
import hashlib
import io as _io

with _ctx.redirect_stdout(_io.StringIO()):
    import ma_nguon_6_01_ntt_va_intt_chung_cho as mn601
    import ma_nguon_6_02_phep_nhan_trong_mien_ntt as mn602
    import ma_nguon_8_01_vong_lap_ky_cua_ml as mn801

# Ma nguon 6.2 dung cac ten toan cuc cua Ma nguon 6.1
mn602.KEM, mn602.DSA, mn602.bitrev = mn601.KEM, mn601.DSA, mn601.bitrev

DSA = mn601.DSA
Q = DSA["q"]
N = 256
D = 13

# (k, l, eta, tau, lambda, gamma1, gamma2, omega) - Bang 8.x (FIPS 204 Bang 1)
THAM_SO = {
    "ML-DSA-44": (4, 4, 2, 39, 128, 2**17, (Q - 1) // 88, 80),
    "ML-DSA-65": (6, 5, 4, 49, 192, 2**19, (Q - 1) // 32, 55),
    "ML-DSA-87": (8, 7, 2, 60, 256, 2**19, (Q - 1) // 32, 75),
}


# ---------------------------------------------------------------- bam
def H(x, n):
    """H = SHAKE256, n byte dau ra."""
    return hashlib.shake_256(x).digest(n)


def G(x, n):
    """G = SHAKE128, n byte dau ra."""
    return hashlib.shake_128(x).digest(n)


class _Luong:
    """Luong XOF: doc dan tung khoi byte (squeeze)."""
    def __init__(self, ham, x, khoi):
        self.ham, self.x, self.buf, self.pos, self.khoi = ham, x, b"", 0, khoi

    def doc(self, n):
        while self.pos + n > len(self.buf):
            self.buf = self.ham(self.x).digest(len(self.buf) + self.khoi)
        out = self.buf[self.pos:self.pos + n]
        self.pos += n
        return out


# ---------------------------------------------------------------- da thuc
def ntt(f):
    return mn601.ntt(f, DSA)


def intt(f):
    return mn601.intt(f, DSA)


pmul = mn602.multiply_ntts_dsa


def ntt_vec(v):
    return [ntt(p) for p in v]


def padd(a, b):
    return [(x + y) % Q for x, y in zip(a, b)]


def psub(a, b):
    return [(x - y) % Q for x, y in zip(a, b)]


def sum_pmul(hang, vhat):
    """Tich vo huong trong mien NTT: sum_j A[i][j] o vhat[j]."""
    acc = [0] * N
    for a, b in zip(hang, vhat):
        acc = [(x + y) % Q for x, y in zip(acc, pmul(a, b))]
    return acc


def mod_pm(r, m):
    """Du tam: r0 trong (-m/2, m/2]."""
    r0 = r % m
    return r0 - m if r0 > m // 2 else r0


def inf_norm(v):
    """Chuan vo cung cua vector da thuc (he so hieu theo du tam modulo q)."""
    return max(abs(mod_pm(x, Q)) for p in v for x in p)


# ---------------------------------------------------------------- lay mau
def rej_ntt_poly(seed):
    """RejNTTPoly (FIPS 204 TT 30, 14)."""
    s, a = _Luong(hashlib.shake_128, seed, 168 * 5), []
    while len(a) < N:
        b0, b1, b2 = s.doc(3)
        z = ((b2 & 127) << 16) | (b1 << 8) | b0
        if z < Q:
            a.append(z)
    return a


def expand_A(rho, k, l):
    """ExpandA (TT 32): A[r][s] = RejNTTPoly(rho || s || r)."""
    return [[rej_ntt_poly(rho + bytes([s, r])) for s in range(l)]
            for r in range(k)]


def _coeff_half_byte(b, eta):
    if eta == 2 and b < 15:
        return 2 - (b % 5)
    if eta == 4 and b < 9:
        return 4 - b
    return None


def rej_bounded_poly(seed, eta):
    """RejBoundedPoly (TT 31, 15): he so co dau trong [-eta, eta]."""
    s, a = _Luong(hashlib.shake_256, seed, 136 * 2), []
    while len(a) < N:
        z = s.doc(1)[0]
        for b in (z & 15, z >> 4):
            c = _coeff_half_byte(b, eta)
            if c is not None and len(a) < N:
                a.append(c)
    return a


def expand_S(rhop, k, l, eta):
    """ExpandS (TT 33)."""
    s1 = [rej_bounded_poly(rhop + r.to_bytes(2, "little"), eta) for r in range(l)]
    s2 = [rej_bounded_poly(rhop + (r + l).to_bytes(2, "little"), eta) for r in range(k)]
    return s1, s2


def expand_mask(rhopp, kappa, l, g1):
    """ExpandMask (TT 34): he so trong [-g1+1, g1], luu o dang modulo q."""
    c = 1 + (g1 - 1).bit_length()
    y = []
    for r in range(l):
        v = H(rhopp + (kappa + r).to_bytes(2, "little"), 32 * c)
        y.append([x % Q for x in bit_unpack(v, g1 - 1, g1)])
    return y


def sample_in_ball(ctil, tau, lam):
    """SampleInBall (TT 29): tau he so +-1, xao tron Fisher-Yates.
    Ban chinh thuc FIPS 204 bam toan bo ctil (lam/4 byte)."""
    s = _Luong(hashlib.shake_256, ctil, 136)
    h = int.from_bytes(s.doc(8), "little")
    c = [0] * N
    for i in range(N - tau, N):
        j = s.doc(1)[0]
        while j > i:
            j = s.doc(1)[0]
        c[i] = c[j]
        c[j] = 1 - 2 * ((h >> (i + tau - N)) & 1)
    return c


# ---------------------------------------------------------------- lam tron
def power2round(r):
    """Power2Round (TT 35)."""
    rp = r % Q
    r0 = mod_pm(rp, 1 << D)
    return (rp - r0) >> D, r0


def decompose(r, g2):
    """Decompose (TT 36)."""
    rp = r % Q
    r0 = mod_pm(rp, 2 * g2)
    if rp - r0 == Q - 1:
        return 0, r0 - 1
    return (rp - r0) // (2 * g2), r0


def high_bits(r, g2):
    return decompose(r, g2)[0]


def low_bits(r, g2):
    return decompose(r, g2)[1]


def make_hint(z, r, g2):
    """MakeHint (TT 39)."""
    return int(high_bits(r, g2) != high_bits(r + z, g2))


def use_hint(h, r, g2):
    """UseHint (TT 40)."""
    m = (Q - 1) // (2 * g2)
    r1, r0 = decompose(r, g2)
    if h == 1:
        return (r1 + 1) % m if r0 > 0 else (r1 - 1) % m
    return r1


def make_hint_vec(ct0, w, cs2, g2):
    """h = MakeHint(-c t0, w - c s2 + c t0) theo tung he so (TT 7 dong 26)."""
    return [[make_hint(-a, b - c + a, g2) for a, b, c in zip(ct0[i], w[i], cs2[i])]
            for i in range(len(w))]


# ---------------------------------------------------------------- dong goi
def _pack_bits(vals, nbit):
    x = 0
    for i, v in enumerate(vals):
        x |= v << (i * nbit)
    return x.to_bytes(len(vals) * nbit // 8, "little")


def _unpack_bits(buf, nbit):
    x, m = int.from_bytes(buf, "little"), (1 << nbit) - 1
    return [(x >> (i * nbit)) & m for i in range(len(buf) * 8 // nbit)]


def simple_bit_pack(w, b):
    """SimpleBitPack (TT 16): he so trong [0, b]."""
    return _pack_bits(w, b.bit_length())


def simple_bit_unpack(v, b):
    return _unpack_bits(v, b.bit_length())


def bit_pack(w, a, b):
    """BitPack (TT 17): he so co dau trong [-a, b], ma hoa b - w_i."""
    return _pack_bits([b - mod_pm(x, Q) for x in w], (a + b).bit_length())


def bit_unpack(v, a, b):
    """BitUnpack (TT 19): tra ve he so co dau."""
    return [b - x for x in _unpack_bits(v, (a + b).bit_length())]


def hint_bit_pack(h, k, om):
    """HintBitPack (TT 20)."""
    y, idx = bytearray(om + k), 0
    for i in range(k):
        for j in range(N):
            if h[i][j]:
                y[idx] = j
                idx += 1
        y[om + i] = idx
    return bytes(y)


def hint_bit_unpack(y, k, om):
    """HintBitUnpack (TT 21): None neu ma hoa sai dang."""
    h, idx = [[0] * N for _ in range(k)], 0
    for i in range(k):
        if y[om + i] < idx or y[om + i] > om:
            return None
        first = idx
        while idx < y[om + i]:
            if idx > first and y[idx - 1] >= y[idx]:
                return None
            h[i][y[idx]] = 1
            idx += 1
    if any(y[i] for i in range(idx, om)):
        return None
    return h


def pk_encode(rho, t1):
    """pkEncode (TT 22): t1 moi he so 10 bit."""
    return rho + b"".join(simple_bit_pack(p, 1023) for p in t1)


def pk_decode(pk, k):
    rho, t1 = pk[:32], []
    for i in range(k):
        t1.append(simple_bit_unpack(pk[32 + 320 * i: 32 + 320 * (i + 1)], 1023))
    return rho, t1


def sk_encode(rho, K, tr, s1, s2, t0, eta):
    out = rho + K + tr
    out += b"".join(bit_pack(p, eta, eta) for p in s1)
    out += b"".join(bit_pack(p, eta, eta) for p in s2)
    out += b"".join(bit_pack(p, 2**(D - 1) - 1, 2**(D - 1)) for p in t0)
    return out


def sk_decode(sk, k, l, eta):
    rho, K, tr = sk[:32], sk[32:64], sk[64:128]
    ls = 32 * (2 * eta).bit_length()
    pos, s1, s2, t0 = 128, [], [], []
    for _ in range(l):
        s1.append(bit_unpack(sk[pos:pos + ls], eta, eta)); pos += ls
    for _ in range(k):
        s2.append(bit_unpack(sk[pos:pos + ls], eta, eta)); pos += ls
    for _ in range(k):
        t0.append(bit_unpack(sk[pos:pos + 32 * D], 2**(D - 1) - 1, 2**(D - 1)))
        pos += 32 * D
    return rho, K, tr, s1, s2, t0


def w1_encode(w1, k, g2):
    """w1Encode (TT 28)."""
    b = (Q - 1) // (2 * g2) - 1
    return b"".join(simple_bit_pack(p, b) for p in w1)


def sig_encode(ctil, z, h, k, l, om, g1):
    """sigEncode (TT 26): z dua ve bieu dien co dau trong bit_pack."""
    out = ctil + b"".join(bit_pack(p, g1 - 1, g1) for p in z)
    return out + hint_bit_pack(h, k, om)


def sig_decode(sig, k, l, om, g1, lam):
    lc = lam // 4
    lz = 32 * (1 + (g1 - 1).bit_length())
    ctil, z = sig[:lc], []
    for i in range(l):
        z.append([x % Q for x in bit_unpack(sig[lc + lz * i: lc + lz * (i + 1)], g1 - 1, g1)])
    h = hint_bit_unpack(sig[lc + lz * l:], k, om)
    return ctil, z, h


# ---------------------------------------------------------------- KeyGen / Sign / Verify
def keygen_internal(xi, ten):
    """ML-DSA.KeyGen_internal (TT 6)."""
    k, l, eta = THAM_SO[ten][:3]
    m = H(xi + bytes([k, l]), 128)
    rho, rhop, K = m[:32], m[32:96], m[96:]
    A = expand_A(rho, k, l)
    s1, s2 = expand_S(rhop, k, l, eta)
    s1h = ntt_vec(s1)
    t = [padd(intt(sum_pmul(A[i], s1h)), s2[i]) for i in range(k)]
    t1 = [[power2round(x)[0] for x in p] for p in t]
    t0 = [[power2round(x)[1] for x in p] for p in t]
    pk = pk_encode(rho, t1)
    tr = H(pk, 64)
    return pk, sk_encode(rho, K, tr, s1, s2, t0, eta)


def format_msg(M, ctx=b""):
    """M' = 0 || |ctx| || ctx || M (ML-DSA thuan, TT 2 dong 10)."""
    assert len(ctx) <= 255
    return bytes([0, len(ctx)]) + ctx + M


def sign(sk, M, ctx, rnd, ten):
    """ML-DSA.Sign (TT 2), giao dien ngoai; rnd = 32 byte 0 cho che do tat dinh."""
    return mn801.sign_internal(sk, format_msg(M, ctx), rnd, ten)


def verify_internal(pk, Mp, sig, ten):
    """ML-DSA.Verify_internal (TT 8)."""
    k, l, eta, tau, lam, g1, g2, om = THAM_SO[ten]
    beta = tau * eta
    if len(pk) != 32 + 320 * k:
        return False
    if len(sig) != lam // 4 + l * 32 * (1 + (g1 - 1).bit_length()) + om + k:
        return False
    rho, t1 = pk_decode(pk, k)
    ctil, z, h = sig_decode(sig, k, l, om, g1, lam)
    if h is None:
        return False
    A = expand_A(rho, k, l)
    tr = H(pk, 64)
    mu = H(tr + Mp, 64)
    ch = ntt(sample_in_ball(ctil, tau, lam))
    zh = ntt_vec(z)
    w1 = []
    for i in range(k):
        ct1 = pmul(ch, ntt([x << D for x in t1[i]]))
        wa = intt(psub(sum_pmul(A[i], zh), ct1))
        w1.append([use_hint(hb, x, g2) for hb, x in zip(h[i], wa)])
    return inf_norm(z) < g1 - beta and ctil == H(mu + w1_encode(w1, k, g2), lam // 4)


def verify(pk, M, sig, ctx, ten):
    return verify_internal(pk, format_msg(M, ctx), sig, ten)


# Gan cac ham phu vao module cua Ma nguon 8.1 de sign_internal goi duoc
for _ten in ("THAM_SO", "sk_decode", "ntt_vec", "expand_A", "H", "expand_mask",
             "intt", "sum_pmul", "high_bits", "w1_encode", "sample_in_ball", "ntt",
             "pmul", "padd", "low_bits", "psub", "inf_norm", "make_hint_vec",
             "sig_encode"):
    setattr(mn801, _ten, globals()[_ten])
