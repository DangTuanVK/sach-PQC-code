# Mã nguồn 20.1c - (khối mã không đánh số, sau Mã nguồn 20.1)
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 20, trang 372
# Trích tự động từ chapters/ch20/main.tex (dòng 345) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 20.1a, Mã nguồn 20.1, Mã nguồn 20.1b ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_20_01a_doan_ma_mo_dau import *  # noqa
    from ma_nguon_20_01_bfv_thu_nho_sinh_khoa import *  # noqa
    from ma_nguon_20_01b_bfv_thu_nho_sinh_khoa_tiep import *  # noqa
# --- Hết phần thêm ---

def bien_do_nhieu(ct, s, m):
    """Chuan vo cuc cua (c0 + c1*s + ...) - Delta*m, lay dai dien tam."""
    return max(abs(modpm(x - D * (y % t))) for x, y in zip(pha(ct, s), m))

rng = random.Random(2026)
pk, s = keygen(rng)
hai = [2] + [0] * (n - 1)                    # ban ro: da thuc hang 2
ct, m = encrypt(pk, hai, rng), hai
for L in range(4):                           # nhan lien tiep voi Enc(2)
    if L > 0:
        ct, m = nhan_bm(ct, encrypt(pk, hai, rng)), [2 * x for x in m]
    kq = decrypt(ct, s)
    print(L, len(ct), m[0], bien_do_nhieu(ct, s, m),
          "dung" if kq == [x % t for x in m] else "SAI: %d" % kq[0])
ct, m = encrypt(pk, hai, rng), hai
for k in range(9):                           # cong lien tiep Enc(2)
    if k > 0:
        ct = [cong(x, y) for x, y in zip(ct, encrypt(pk, hai, rng))]
        m = [x + y for x, y in zip(m, hai)]
    if k in (0, 1, 4, 8):
        print("cong", k, bien_do_nhieu(ct, s, m), decrypt(ct, s) == m)
