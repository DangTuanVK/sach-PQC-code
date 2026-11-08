# Mã nguồn 18.1c - (khối mã không đánh số, sau Mã nguồn 18.1)
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 18, trang 357
# Trích tự động từ chapters/ch19/main.tex (dòng 294) bằng extract.py; không sửa tay file này.

# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 18.1, Mã nguồn 18.1b ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_18_01_phan_loi_cua_cong_cu import *  # noqa
    from ma_nguon_18_01b_phan_loi_cua_cong_cu_tiep import *  # noqa
# --- Hết phần thêm ---

def xuat_cbom(kq, hom_nay):
    return {"bomFormat": "CycloneDX", "specVersion": "1.6",
        "metadata": {"timestamp": hom_nay.isoformat()},
        "components": [
            {"type": "cryptographic-asset",
             "name": r["ten"],
             "cryptoProperties": {
                 "assetType": "certificate",
                 "certificateProperties": {
                     "certificateFormat": "X.509",
                     "notValidAfter": r["het"].isoformat()}},
             "properties": [
                 {"name": "thuat_toan_khoa", "value": r["alg"]},
                 {"name": "diem_uu_tien", "value": str(r["diem"])}]}
            for r in kq]}

if __name__ == "__main__":
    hom_nay = datetime.utcnow()
    kq = kiem_ke(sys.argv[1], hom_nay)
    in_bao_cao(kq, hom_nay)
    json.dump(xuat_cbom(kq, hom_nay), open("cbom.json", "w"), indent=2)
