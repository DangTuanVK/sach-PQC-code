# Mã nguồn 11.1 - Tính kích thước chữ ký SLH-DSA từ công thức trong đặc tả, sau đó đối chiếu với bảng tham số công bố.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 11, trang 261
# Trích tự động từ chapters/ch11/main.tex (dòng 1034) bằng extract.py; không sửa tay file này.

from math import ceil, floor, log2

def wots_len(n, lgw):                  # so chuoi WOTS+, RFC 8391
    w = 1 << lgw
    len1 = ceil(8*n / lgw)
    len2 = floor(log2(len1 * (w-1)) / lgw) + 1
    return len1 + len2

def sig_size(n, h, d, a, k, lgw):
    """|sig| = |R| + |sig_FORS| + |sig_HT|  (FIPS 205)."""
    L = wots_len(n, lgw)
    return n + k*(a+1)*n + (h + d*L)*n

FIPS205 = {   # ten: (n, h, d, a, k, lgw) -> (|pk| cong bo, |sig| cong bo)
    "SLH-DSA-128s": ((16, 63,  7, 12, 14, 4), (32,  7856)),
    "SLH-DSA-128f": ((16, 66, 22,  6, 33, 4), (32, 17088)),
    "SLH-DSA-192s": ((24, 63,  7, 14, 17, 4), (48, 16224)),
    "SLH-DSA-192f": ((24, 66, 22,  8, 33, 4), (48, 35664)),
    "SLH-DSA-256s": ((32, 64,  8, 14, 22, 4), (64, 29792)),
    "SLH-DSA-256f": ((32, 68, 17,  9, 35, 4), (64, 49856)),
}
print("bo tham so    len  |pk| tinh  cong bo  |sig| tinh  cong bo  ket qua")
for ten, (ts, (pkc, sgc)) in FIPS205.items():
    pk, sg = 2*ts[0], sig_size(*ts)        # pk = PK.seed || PK.root
    ok = "OK" if (pk, sg) == (pkc, sgc) else "SAI"
    print(f"{ten}  {wots_len(ts[0], ts[5]):3}  {pk:9}  {pkc:7}  "
          f"{sg:10}  {sgc:7}  {ok}")
