# Không có trong sách: chương trình đối chiếu NTT với phép nhân trực tiếp, đo thời gian và hai phép kiểm riêng. Tái tạo kết quả in sau Mã nguồn 6.3 (chapters/ch6/main.tex).
import random
import time

import ma_nguon_6_01_ntt_va_intt_chung_cho as mn1
import ma_nguon_6_02_phep_nhan_trong_mien_ntt as mn2
import ma_nguon_6_03_phep_nhan_truc_tiep_trong as mn3

# Ma nguon 6.2 dung KEM, DSA, bitrev cua Ma nguon 6.1
mn2.KEM, mn2.DSA, mn2.bitrev = mn1.KEM, mn1.DSA, mn1.bitrev

KEM, DSA = mn1.KEM, mn1.DSA
ntt, intt, bitrev = mn1.ntt, mn1.intt, mn1.bitrev
nhan_truc_tiep = mn3.nhan_truc_tiep

SO_CAP = 200
SO_LAN_DO = 50
rng = random.Random(2026)


def nhan_qua_ntt(f, g, P, nhan_mien_ntt):
    return intt(nhan_mien_ntt(ntt(f, P), ntt(g, P)), P)


for ten, P, nhan_mien_ntt in (("ML-KEM", KEM, mn2.multiply_ntts_kem),
                              ("ML-DSA", DSA, mn2.multiply_ntts_dsa)):
    q = P["q"]
    da_thuc = lambda: [rng.randrange(q) for _ in range(256)]
    cap = [(da_thuc(), da_thuc()) for _ in range(SO_CAP)]
    khop = sum(nhan_qua_ntt(f, g, P, nhan_mien_ntt) == nhan_truc_tiep(f, g, q)
               for f, g in cap)
    print(f"[{ten}] doi chieu NTT vs nhan truc tiep: {khop}/{SO_CAP} trung khop")
    f = da_thuc()
    print(f"[{ten}] INTT(NTT(f)) == f : {intt(ntt(f, P), P) == f}")
    do = cap[:SO_LAN_DO]
    t0 = time.perf_counter()
    for f, g in do:
        nhan_truc_tiep(f, g, q)
    t_tt = time.perf_counter() - t0
    t0 = time.perf_counter()
    for f, g in do:
        nhan_qua_ntt(f, g, P, nhan_mien_ntt)
    t_ntt = time.perf_counter() - t0
    print(f"[{ten}] {SO_LAN_DO} phep nhan: truc tiep {t_tt:.3f}s | qua NTT {t_ntt:.3f}s"
          f" | nhanh gap {t_tt / t_ntt:.1f} lan")

# Kiem ML-DSA theo dinh nghia: w_hat[i] = w(zeta^(2*BitRev8(i)+1))
q = DSA["q"]
w = [rng.randrange(q) for _ in range(256)]
w_hat = ntt(w, DSA)


def gia_tri(w, x, q):
    """Tinh w(x) mod q theo luoc do Horner."""
    y = 0
    for he_so in reversed(w):
        y = (y * x + he_so) % q
    return y


dung = all(w_hat[i] == gia_tri(w, pow(DSA["zeta"], 2 * bitrev(i, 8) + 1, q), q)
           for i in range(256))
print(f"[ML-DSA] w_hat[i] == w(zeta^(2*BitRev8(i)+1)) voi moi i: {dung}")

# Quet toan bo Z_3329 tim can nguyen thuy bac 512 (x^256 = -1)
q = KEM["q"]
co_can = any(pow(x, 256, q) == q - 1 for x in range(1, q))
print(f"[ML-KEM] q mod 512 = {q % 512}, co can bac 512: {co_can}")
