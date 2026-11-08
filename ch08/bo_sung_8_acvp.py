# Không có trong sách: doi chieu ML-DSA voi vector ACVP cua NIST (keyGen, sigGen thuan giao dien ngoai). Tái tạo kết quả in sau Mã nguồn 8.1 (chapters/ch8/main.tex).
import json
from pathlib import Path

import bo_sung_8_mldsa as dsa

ACVP = Path(__file__).resolve().parent.parent / "du_lieu" / "acvp"
BO = ("ML-DSA-44", "ML-DSA-65", "ML-DSA-87")


def doc(ten):
    return json.loads((ACVP / ten).read_text())["testGroups"]


# --- keyGen: tu mam xi tinh lai (pk, sk), so tung byte
dat = tong = 0
for g in doc("ML-DSA-keyGen-FIPS204.internalProjection.json"):
    for t in g["tests"]:
        pk, sk = dsa.keygen_internal(bytes.fromhex(t["seed"]), g["parameterSet"])
        tong += 1
        dat += pk.hex().upper() == t["pk"].upper() and sk.hex().upper() == t["sk"].upper()
print(f"[KAT] keyGen day du: {dat}/{tong}")

# --- sigGen: chi cac nhom thuan (khong tien bam), giao dien ngoai, mu tinh ben trong
nhom = [g for g in doc("ML-DSA-sigGen-FIPS204.internalProjection.json")
        if g["signatureInterface"] == "external" and g["preHash"] == "pure"
        and not g["externalMu"]]
for tat_dinh, tieu_de in ((True, "thuan, tat dinh, giao dien ngoai"),
                          (False, "thuan, co rao, rnd cho san trong vector")):
    print(f"\n[KAT] sigGen ({tieu_de}):")
    for ten in BO:
        dat = tong = 0
        for g in nhom:
            if g["parameterSet"] != ten or g["deterministic"] != tat_dinh:
                continue
            for t in g["tests"]:
                sk, pk = bytes.fromhex(t["sk"]), bytes.fromhex(t["pk"])
                M, ctx = bytes.fromhex(t["message"]), bytes.fromhex(t["context"])
                rnd = bytes(32) if tat_dinh else bytes.fromhex(t["rnd"])
                sig = dsa.sign(sk, M, ctx, rnd, ten)
                tong += 1
                # khop tung byte voi vector, va chu ky phai qua Verify
                dat += (sig.hex().upper() == t["signature"].upper()
                        and dsa.verify(pk, M, sig, ctx, ten))
        print(f"   {ten}: {dat}/{tong}")
