# Không có trong sách: chay vong doi McEliece thu nho (sinh khoa, ma hoa, giai ma Patterson) voi ba bo tham so. Tái tạo kết quả in sau Mã nguồn 11.1 (chapters/ch12/main.tex).
import random
import time

from bo_sung_11_mceliece import Goppa

HAT_GIONG = 2026
SO_LAN = 30
rng = random.Random(HAT_GIONG)

print("  m   t    n    k  |pk| (B)  giai ma dung  thoi gian")
for m, t, n in [(6, 3, 64), (6, 5, 64), (6, 8, 64)]:
    t0 = time.perf_counter()
    ht = Goppa(m, t, n, rng)                   # sinh khoa
    dung = 0
    for _ in range(SO_LAN):                    # ma hoa, giai ma SO_LAN lan
        e, s = ht.ma_hoa()
        if ht.giai_ma(s) == e:
            dung += 1
    dt = time.perf_counter() - t0
    print(f"{m:3d} {t:3d} {n:4d} {ht.k:4d} {ht.kich_thuoc_pk():9d} "
          f"{dung:>9d}/{SO_LAN:<2d} {dt:9.1f}s")
