# Không có trong sách: đếm ứng viên bị loại của SampleNTT trong 20 lần sinh khóa ML-KEM-768. Tái tạo kết quả in sau Mã nguồn 7.2 (chapters/ch7/main.tex).
import random
from hashlib import shake_128

import bo_sung_7_mlkem as kem

HAT_GIONG = 2026          # sach khong neu nguon ngau nhien; chon hat giong co dinh
SO_LAN = 20
q = kem.q

sample_ntt_goc = kem.m72b.sample_ntt
dem = {"he_so": 0, "ung_vien": 0}


def dem_ung_vien(seed32, j, i):
    """Doc lai luong SHAKE128 nhu sample_ntt: moi bo ba byte cho 2 ung vien."""
    buf = shake_128(seed32 + bytes([j, i])).digest(3 * 800)
    a, p, uv = [], 0, 0
    while len(a) < 256:
        C0, C1, C2 = buf[p], buf[p + 1], buf[p + 2]; p += 3
        d1, d2 = C0 + 256 * (C1 % 16), (C1 >> 4) + 16 * C2
        uv += 2
        if d1 < q:
            a.append(d1)
        if d2 < q and len(a) < 256:
            a.append(d2)
    return a, uv


def sample_ntt_dem(seed32, j, i):
    """Goi ham cua sach (Ma nguon 7.2b) va dem so ung vien da doc."""
    a = sample_ntt_goc(seed32, j, i)
    a2, uv = dem_ung_vien(seed32, j, i)
    assert a == a2
    dem["he_so"] += len(a)
    dem["ung_vien"] += uv
    return a


kem.m72b.sample_ntt = sample_ntt_dem
rng = random.Random(HAT_GIONG)
for _ in range(SO_LAN):
    d, z = rng.randbytes(32), rng.randbytes(32)
    kem.keygen_internal(d, z, "ML-KEM-768")
kem.m72b.sample_ntt = sample_ntt_goc

tu_choi = 1 - dem["he_so"] / dem["ung_vien"]
print(f"[lay mau tu choi] {dem['he_so']} he so lay tu {dem['ung_vien']} ung vien")
print(f"                  -> ti le tu choi {100 * tu_choi:.2f}%")
print(f"  ly thuyet: 1 - q/2^12 = {100 * (1 - q / 2**12):.2f}%")
