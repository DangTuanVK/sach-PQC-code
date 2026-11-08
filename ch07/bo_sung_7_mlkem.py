# Không có trong sách: phần còn lại của cài đặt ML-KEM (băm, ByteEncode/ByteDecode, Compress, CBD, K-PKE, keygen_internal) để chạy Mã nguồn 7.2, 7.2b, 7.2c (chapters/ch7/main.tex).
"""Module phu tro: cai cac ham ma Ma nguon 7.2, 7.2b, 7.2c goi nhung sach khong in,
theo dung Thuat toan 3-8, 13-16 cua FIPS 203 (tom tat o Muc 7.2 cua sach), roi gan
vao module cua sach. NTT, INTT va phep nhan co so lay tu Ma nguon 6.1, 6.2."""
import contextlib
import hashlib
import io
from hashlib import shake_128, shake_256

with contextlib.redirect_stdout(io.StringIO()):
    import ma_nguon_6_01_ntt_va_intt_chung_cho as m61
    import ma_nguon_6_02_phep_nhan_trong_mien_ntt as m62
    import ma_nguon_7_02_hai_ham_cua_lop_ngoai as m72
    import ma_nguon_7_02b_hai_ham_cua_lop_ngoai_tiep as m72b

KEM = m61.KEM
q = KEM["q"]
# Ma nguon 6.2 dung KEM, bitrev cua Ma nguon 6.1
m62.KEM, m62.bitrev = KEM, m61.bitrev

# Bang 7.x cua sach: (k, eta1, eta2, du, dv)
THAM_SO = {"ML-KEM-512": (2, 3, 2, 10, 4),
           "ML-KEM-768": (3, 2, 2, 10, 4),
           "ML-KEM-1024": (4, 2, 2, 11, 5)}


# --- Ham bam (Muc 4.1 FIPS 203, Bang ham bam cua sach) ---
def G(s):
    """SHA3-512, tach thanh hai nua 32 byte."""
    h = hashlib.sha3_512(s).digest()
    return h[:32], h[32:]


def H(s):
    return hashlib.sha3_256(s).digest()


def J(s):
    return shake_256(s).digest(32)


def PRF(eta, s, b):
    return shake_256(s + bytes([b])).digest(64 * eta)


# --- ByteEncode / ByteDecode (Thuat toan 3-6) ---
def byte_encode(F, d):
    bits = 0
    for i, a in enumerate(F):
        bits |= (a % (1 << d)) << (i * d)
    return bits.to_bytes(32 * d, "little")


def byte_decode(B, d):
    bits = int.from_bytes(B, "little")
    m = q if d == 12 else 1 << d
    return [((bits >> (i * d)) & ((1 << d) - 1)) % m for i in range(256)]


# --- Compress / Decompress (cong thuc nguyen cua sach) ---
def compress(x, d):
    return ((x << (d + 1)) + q) // (2 * q) % (1 << d)


def decompress(y, d):
    return (q * y + (1 << (d - 1))) >> d


# --- SamplePolyCBD (Thuat toan 8) ---
def sample_poly_cbd(B, eta):
    bits = int.from_bytes(B, "little")
    f = []
    for i in range(256):
        x = sum((bits >> (2 * i * eta + j)) & 1 for j in range(eta))
        y = sum((bits >> (2 * i * eta + eta + j)) & 1 for j in range(eta))
        f.append((x - y) % q)
    return f


# --- Phep tinh tren vector da thuc ---
def ntt(f):
    return m61.ntt(f, KEM)


def intt(f):
    return m61.intt(f, KEM)


def cong(f, g):
    return [(a + b) % q for a, b in zip(f, g)]


def tich_vo_huong(u, v):
    """Tong cac tich MultiplyNTTs trong mien NTT."""
    kq = [0] * 256
    for a, b in zip(u, v):
        kq = cong(kq, m62.multiply_ntts_kem(a, b))
    return kq


def sinh_ma_tran(rho, k):
    """A[i][j] = SampleNTT(rho || j || i), Ma nguon 7.2b."""
    return [[m72b.sample_ntt(rho, j, i) for j in range(k)] for i in range(k)]


# --- K-PKE (Thuat toan 13-15) ---
def kpke_keygen(d, k, eta1):
    rho, sigma = G(d + bytes([k]))
    A = sinh_ma_tran(rho, k)
    s = [sample_poly_cbd(PRF(eta1, sigma, i), eta1) for i in range(k)]
    e = [sample_poly_cbd(PRF(eta1, sigma, k + i), eta1) for i in range(k)]
    s_hat = [ntt(x) for x in s]
    e_hat = [ntt(x) for x in e]
    t_hat = [cong(tich_vo_huong(A[i], s_hat), e_hat[i]) for i in range(k)]
    ek = b"".join(byte_encode(t, 12) for t in t_hat) + rho
    dk = b"".join(byte_encode(x, 12) for x in s_hat)
    return ek, dk


def kpke_encrypt(ek, m, r, k, eta1, eta2, du, dv):
    t_hat = [byte_decode(ek[384 * i:384 * (i + 1)], 12) for i in range(k)]
    rho = ek[384 * k:384 * k + 32]
    A = sinh_ma_tran(rho, k)
    y = [sample_poly_cbd(PRF(eta1, r, i), eta1) for i in range(k)]
    e1 = [sample_poly_cbd(PRF(eta2, r, k + i), eta2) for i in range(k)]
    e2 = sample_poly_cbd(PRF(eta2, r, 2 * k), eta2)
    y_hat = [ntt(x) for x in y]
    u = [cong(intt(tich_vo_huong([A[j][i] for j in range(k)], y_hat)), e1[i])
         for i in range(k)]                         # A^T o y
    mu = [decompress(b, 1) for b in byte_decode(m, 1)]
    v = cong(cong(intt(tich_vo_huong(t_hat, y_hat)), e2), mu)
    c1 = b"".join(byte_encode([compress(x, du) for x in ui], du) for ui in u)
    c2 = byte_encode([compress(x, dv) for x in v], dv)
    return c1 + c2


def kpke_decrypt(dk, c, k, du, dv):
    c1, c2 = c[:32 * du * k], c[32 * du * k:]
    u = [[decompress(x, du) for x in byte_decode(c1[32 * du * i:32 * du * (i + 1)], du)]
         for i in range(k)]
    v = [decompress(x, dv) for x in byte_decode(c2, dv)]
    s_hat = [byte_decode(dk[384 * i:384 * (i + 1)], 12) for i in range(k)]
    su = intt(tich_vo_huong(s_hat, [ntt(x) for x in u]))
    w = [(a - b) % q for a, b in zip(v, su)]
    return byte_encode([compress(x, 1) for x in w], 1)


# --- ML-KEM.KeyGen_internal (Thuat toan 16) ---
def keygen_internal(d, z, ten):
    k, eta1, eta2, du, dv = THAM_SO[ten]
    ek, dkp = kpke_keygen(d, k, eta1)
    return ek, dkp + ek + H(ek) + z


# Gan vao cac module cua sach
m72.THAM_SO, m72.G, m72.H, m72.J = THAM_SO, G, H, J
m72.kpke_encrypt, m72.kpke_decrypt = kpke_encrypt, kpke_decrypt
m72b.shake_128, m72b.q = shake_128, q

encaps_internal = m72.encaps_internal
decaps_internal = m72.decaps_internal
sample_ntt = m72b.sample_ntt
