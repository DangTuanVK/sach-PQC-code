# Không có trong sách: các hàm phụ trợ vec, nhieu, tich, G, H, bam_ct và bốn thí nghiệm. Tái tạo kết quả in sau Mã nguồn 3.2 (chapters/ch3/main.tex).
import hashlib
import random

import ma_nguon_3_01_he_ma_hoa_thu_nho as pke
import ma_nguon_3_01b_he_ma_hoa_thu_nho_tiep as cca
import ma_nguon_3_02_boc_bien_doi_fo_quanh as fo
import ma_nguon_3_02b_boc_bien_doi_fo_quanh_tiep as nghe

q, n, sigma = pke.q, pke.n, pke.sigma
SO_LAN = 500
HAT_GIONG = 2026


# --- Cac ham phu tro khong in trong sach ---
def vec(rng, k):
    """Vector k phan tu ngau nhien deu trong Z_q."""
    return [rng.randrange(q) for _ in range(k)]


def nhieu(rng):
    """Nhieu nho: Gauss roi rac lam tron, do lech chuan sigma."""
    return round(rng.gauss(0, sigma))


def tich(a, b):
    """Tich vo huong modulo q."""
    return sum(x * y for x, y in zip(a, b)) % q


def G(*phan):
    """G = SHA3-512 tren chuoi ghep (64 byte: 32 byte K, 32 byte hat giong r)."""
    return hashlib.sha3_512(b"".join(phan)).digest()


def H(*phan):
    """H = SHA3-256 tren chuoi ghep, dung thay cho J."""
    return hashlib.sha3_256(b"".join(phan)).digest()


def bam_ct(ct):
    """Bam ban ma (u, v) thanh 32 byte."""
    u, v = ct
    return H(b"".join(x.to_bytes(2, "big") for x in list(u) + [v]))


# Gan vao cac module cua sach
pke.vec, pke.nhieu, pke.tich = vec, nhieu, tich
for mod in (cca, fo, nghe):
    mod.q = q
    mod.encrypt, mod.decrypt = pke.encrypt, pke.decrypt
    mod.random = random
    mod.G, mod.H, mod.bam_ct = G, H, bam_ct


def ti_le(k):
    return f"{k:3d}/{SO_LAN} = {100 * k / SO_LAN:.1f}%"


# Thi nghiem 1: tan cong CCA tren PKE tran
rng = random.Random(HAT_GIONG)
dung = 0
for _ in range(SO_LAN):
    pk, sk = pke.keygen(rng)
    m_bi_mat, doan = cca.tan_cong_cca(pk, sk, rng)
    dung += (m_bi_mat == doan)
print(f"[PKE tran]  tan cong CCA doan dung              {ti_le(dung)}")

# Thi nghiem 2-4: KEM + FO
rng = random.Random(HAT_GIONG)
sua_dung = hop_le_dung = nghe_dung = 0
for _ in range(SO_LAN):
    pk, sk = pke.keygen(rng)
    A, b = pk
    h = H(b"".join(x.to_bytes(2, "big") for hang in A for x in hang + [0]),
          b"".join(x.to_bytes(2, "big") for x in b))
    z = rng.randbytes(32)
    ct, K = fo.encaps(pk, h, rng)
    u, v = ct
    ct_khac = (u, (v + q // 2) % q)                     # tan cong cu: lat bit
    sua_dung += (fo.decaps(pk, h, sk, z, ct_khac) == K)
    hop_le_dung += (fo.decaps(pk, h, sk, z, ct) == K)
    nghe_dung += (nghe.nghe_len(pk, h, ct) == K)
print(f"[KEM + FO]  ban ma bi sua cho ra khoa dung      {sua_dung:3d}/{SO_LAN}")
print(f"[KEM + FO]  ban ma hop le giai dong goi dung    {ti_le(hop_le_dung)}")
print(f"[KEM + FO]  nghe len thu dong, |M| = 2          {ti_le(nghe_dung)}")
