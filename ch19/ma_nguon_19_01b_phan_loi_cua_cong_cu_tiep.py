# Mã nguồn 19.1b - (khối mã không đánh số, sau Mã nguồn 19.1)
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 19, trang 359
# Trích tự động từ chapters/ch19/main.tex (dòng 249) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 19.1 ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_19_01_phan_loi_cua_cong_cu import *  # noqa
# --- Hết phần thêm ---

MAU_PEM = re.compile(r"-----BEGIN CERTIFICATE-----.+?"
                     r"-----END CERTIFICATE-----", re.S)

def kiem_ke(tep_pem, hom_nay):
    ket_qua = []
    for pem in MAU_PEM.findall(open(tep_pem).read()):
        alg, bits, het = doc_chung_thu(pem)
        ho, tinh_trang = PHAN_LOAI.get(alg, (alg, "chua phan loai"))
        nam = (het - hom_nay).days / 365.25
        ten = "%s-%d" % (ho, bits) if bits else alg
        ket_qua.append({"ten": ten, "alg": alg, "ho": ho, "bits": bits,
                        "het": het, "tinh_trang": tinh_trang,
                        "diem": diem_uu_tien(ho, bits, nam)})
    return ket_qua

def nhom_het_han(r, hom_nay):
    if r["het"] < hom_nay:  return "da het han"
    if r["het"].year <= 2030: return "het han 2026-2030"
    if r["het"].year <= 2035: return "het han 2031-2035"
    if r["het"].year <= 2040: return "het han 2036-2040"
    return "het han sau 2040"

def in_bao_cao(kq, hom_nay):
    n = len(kq)
    print("Tong so chung thu:", n)
    print("=== Phan bo theo ho thuat toan ===")
    dem = Counter((r["ho"], r["bits"]) for r in kq)
    for (ho, bits), c in dem.most_common():
        print("%-8s %6d %6d %7.1f%%" % (ho, bits, c, 100 * c / n))
    print("=== Ngay het han (tinh tai %s) ===" % hom_nay.date())
    dem = Counter(nhom_het_han(r, hom_nay) for r in kq)
    for nhom in sorted(dem):
        c = dem[nhom]
        print("  %-18s %4d (%5.1f%%)" % (nhom, c, 100 * c / n))
    sau = sum(r["het"].year > 2035 for r in kq)
    print("  con hieu luc SAU 2035: %d (%.1f%%)" % (sau, 100 * sau / n))
