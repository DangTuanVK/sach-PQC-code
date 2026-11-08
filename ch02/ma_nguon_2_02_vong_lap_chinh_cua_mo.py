# Mã nguồn 2.2 - Vòng lặp chính của mô phỏng Shor, dùng các hàm ở Mã nguồn 2.1; vòng lặp cuối in kết quả cho N = 15, 21, 35.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 2, trang 22
# Trích tự động từ chapters/ch2/main.tex (dòng 444) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 2.1 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_2_01_phan_luong_tu_cua_mo import *  # noqa
# --- Hết phần thêm ---

def shor(N, seed=165, so_lan=50):
    rng = random.Random(seed)
    for lan in range(1, so_lan + 1):
        x = rng.randrange(2, N - 1)
        d = gcd(x, N)
        if d > 1:                                # gap may, khong can luong tu
            return d, N // d, lan, None
        q, t, y, tap_a, pho = pho_sau_qft(N, x, rng=rng)
        c = do(pho, rng)                         # do thanh ghi 1
        r = Fraction(c, q).limit_denominator(N).denominator   # phan so lien tuc
        if r % 2 or pow(x, r, N) != 1:
            continue
        p = gcd(pow(x, r//2, N) - 1, N)
        if 1 < p < N:
            return p, N // p, lan, (x, q, t, c, r)
    return None, None, so_lan, None

for N in (15, 21, 35):
    p, p2, lan, (x, q, t, c, r) = shor(N)
    print(f"N={N:3d} -> {p} x {p2:<4} x={x}, q={q:<4} ({t:2d} qubit), "
          f"c={str(c) + ',':<5} r={r}")
