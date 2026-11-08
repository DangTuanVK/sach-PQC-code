# Mã nguồn 4.1 - Tính kích thước khóa và bản mã trực tiếp từ công thức trong văn bản chuẩn, sau đó đối chiếu với bảng công bố.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 4, trang 45
# Trích tự động từ chapters/ch4/main.tex (dòng 295) bằng extract.py; không sửa tay file này.

from math import ceil

def mlkem_kich_thuoc(k, du, dv):                 # FIPS 203 §7
    return 384*k + 32, 768*k + 96, 32*(du*k + dv)

def hqc_kich_thuoc(n, n1, n2, k_bit):            # dac ta HQC §4.2
    seed, salt = 32, 16
    ek = seed + ceil(n/8)
    dk = ek + seed + ceil(k_bit/8) + seed
    ct = ceil(n/8) + ceil(n1*n2/8) + salt
    return ek, dk, ct

def cm_kich_thuoc(m, n, t):                      # Classic McEliece §2, §7
    mt = m*t
    k  = n - mt                                  # T la ma tran mt x k tren F2
    return mt*ceil(k/8), ceil(mt/8)              # (|pk|, |ct|)

def doi_chieu(ten, tinh, cong_bo):
    print(f"  {'OK ' if tinh == cong_bo else 'LECH'} {ten:13s} "
          f"tinh={str(tinh):22s}cong_bo={cong_bo}")

MLKEM = {  # ten: ((k, du, dv), (|ek|, |dk|, |ct|) theo Bang 3 cua FIPS 203)
    "ML-KEM-512":  ((2, 10, 4), (800, 1632, 768)),
    "ML-KEM-768":  ((3, 10, 4), (1184, 2400, 1088)),
    "ML-KEM-1024": ((4, 11, 5), (1568, 3168, 1568)),
}
HQC = {    # ten: ((n, n1, n2, k), (|ek|, |dk|, |ct|) theo dac ta HQC)
    "HQC-1": ((17669, 46, 384, 128), (2241, 2321, 4433)),
    "HQC-3": ((35851, 56, 640, 192), (4514, 4602, 8978)),
    "HQC-5": ((57637, 90, 640, 256), (7237, 7333, 14421)),
}
CM = {"mceliece348864": (12, 3488, 64), "mceliece6960119": (13, 6960, 119),
      "mceliece8192128": (13, 8192, 128)}

print("== ML-KEM (FIPS 203) ==")
for ten, (tham_so, cong_bo) in MLKEM.items():
    doi_chieu(ten, mlkem_kich_thuoc(*tham_so), cong_bo)
print("== HQC (dac ta 2025-08-22) ==")
for ten, (tham_so, cong_bo) in HQC.items():
    doi_chieu(ten, hqc_kich_thuoc(*tham_so), cong_bo)
print("== Classic McEliece ==")
for ten, tham_so in CM.items():
    pk, ct = cm_kich_thuoc(*tham_so)
    so = f"{pk:,d}".replace(",", " ")                       # 261 120
    kib = f"{pk/1024:,.1f}".replace(",", " ").replace(".", ",")  # 255,0
    print(f"  {ten:17s} |pk| = {so:>9s} B ({kib:>7s} KiB)   |ct| = {ct:3d} B")
