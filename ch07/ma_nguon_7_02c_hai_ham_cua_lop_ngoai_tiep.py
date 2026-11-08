# Mã nguồn 7.2c - (khối mã không đánh số, sau Mã nguồn 7.2)
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 7, trang 149
# Trích tự động từ chapters/ch7/main.tex (dòng 1621) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ bo_sung_7_mlkem (tệp bổ sung, không in trong sách) ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from bo_sung_7_mlkem import *  # noqa
# --- Hết phần thêm ---

import json

d = json.load(open("ML-KEM-keyGen-FIPS203.internalProjection.json"))
tong = dung = 0
for g in d["testGroups"]:
    for t in g["tests"]:
        ek, dk = keygen_internal(bytes.fromhex(t["d"]),
                                 bytes.fromhex(t["z"]), g["parameterSet"])
        tong += 1
        dung += (ek.hex().upper() == t["ek"] and dk.hex().upper() == t["dk"])
print(f"keyGen: {dung}/{tong}")
