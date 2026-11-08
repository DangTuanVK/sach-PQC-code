# Mã nguồn 9.2 - Bộ lấy mẫu CDT thoát sớm. Kết quả thống kê giống Mã nguồn 9.1, nhưng số vòng lặp phụ thuộc giá trị trả về.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 9, trang 216
# Trích tự động từ chapters/ch9/main.tex (dòng 978) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 9.1 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_9_01_bo_lay_mau_gauss_roi import *  # noqa
# --- Hết phần thêm ---

def lay_mau_thoat_som(bit=BIT):        # KHONG dung cho muc dich that
    u = secrets.randbits(bit)
    for n, x in CDT:
        if u < n:
            return x                   # thoat som: so vong lap lo gia tri x
    return GIATRI[-1]
