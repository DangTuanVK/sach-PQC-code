# Mã nguồn 20.1b - (khối mã không đánh số, sau Mã nguồn 20.1)
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 20, trang 372
# Trích tự động từ chapters/ch20/main.tex (dòng 299) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 20.1a ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_20_01a_doan_ma_mo_dau import *  # noqa
# --- Hết phần thêm ---

def nhan_bm(c1, c2):
    """Tich tensor roi chia ti le t/q -- buoc nhan cua BFV.
       LUU Y: tich tensor phai tinh TRUOC khi rut gon modulo q,
       neu khong thi phep chia ti le mat thong tin."""
    A = [[modpm(x) for x in p] for p in c1]   # dua ve dai dien tam
    B = [[modpm(x) for x in p] for p in c2]
    d = [[0] * n for _ in range(len(A) + len(B) - 1)]
    for i, a in enumerate(A):                 # thanh phan i+j <-> s^(i+j)
        for j, b in enumerate(B):
            tich = nhan_chinh_xac(a, b)       # KHONG rut gon modulo q
            d[i + j] = [x + y for x, y in zip(d[i + j], tich)]
    return [[((t * x + q // 2) // q) % q for x in p] for p in d]
