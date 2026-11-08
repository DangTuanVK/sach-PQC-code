# Mã nguồn 20.1 - BFV thu nhỏ: sinh khóa, mã hóa và giải mã. So sánh với K-PKE ở Chương 7 sẽ thấy cấu trúc gần như trùng khớp.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 20, trang 372
# Trích tự động từ chapters/ch20/main.tex (dòng 258) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 20.1a ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_20_01a_doan_ma_mo_dau import *  # noqa
# --- Hết phần thêm ---

def keygen(rng):
    s = nhi_phan(rng)                        # khoa bi mat, he so 0/1
    a = ngau_nhien(rng)
    e = nhieu_nho(rng)
    b = modq([-(x + y) for x, y in zip(nhan(a, s), e)])
    return (a, b), s

def encrypt(pk, m, rng):
    a, b = pk
    u  = nhi_phan(rng)                       # ngau nhien cho moi lan ma hoa
    e1, e2 = nhieu_nho(rng), nhieu_nho(rng)
    dm = [D * (x % t) for x in m]            # nhan ban ro voi Delta
    c0 = modq([x + y + z for x, y, z in zip(nhan(b, u), e1, dm)])
    c1 = modq([x + y for x, y in zip(nhan(a, u), e2)])
    return [c0, c1]

def pha(ct, s):
    """c0 + c1*s + c2*s^2 + ... (mod q)."""
    acc, sp = ct[0][:], None
    for i in range(1, len(ct)):
        sp = s[:] if i == 1 else nhan(sp, s)
        acc = cong(acc, nhan(ct[i], sp))
    return acc

def decrypt(ct, s):
    """Chia ti le t/q roi lam tron, hoan toan bang so nguyen."""
    return [((t * modpm(x) + q // 2) // q) % t for x in pha(ct, s)]
