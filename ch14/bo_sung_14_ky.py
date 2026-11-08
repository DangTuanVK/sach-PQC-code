# Không có trong sách: chay ky va xac minh UOV thu nho voi bon cau hinh tren F_16. Tái tạo kết quả in sau Mã nguồn 14.1 (chapters/ch14/main.tex).
import random
import time

from bo_sung_14_uov import UOV

HAT_GIONG = 2026
SO_LAN = 20
rng = random.Random(HAT_GIONG)

print("   n   m   v  |pk| (he so)   ky dung  thoi gian")
for n, m in [(8, 4), (12, 6), (16, 8), (20, 10)]:
    t0 = time.perf_counter()
    ht = UOV(n, m, rng)                        # sinh khoa
    dung = 0
    for _ in range(SO_LAN):
        y = [rng.randrange(16) for _ in range(m)]   # dich ngau nhien
        x = ht.sign(y)
        if ht.verify(x, y):
            dung += 1
    dt = time.perf_counter() - t0
    print(f"{n:4d} {m:3d} {ht.v:3d} {ht.so_he_so_pk():13d} "
          f"{dung:>6d}/{SO_LAN:<2d} {dt:9.1f}s")
