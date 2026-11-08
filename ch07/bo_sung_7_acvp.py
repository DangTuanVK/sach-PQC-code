# Không có trong sách: đối chiếu vector ACVP keyGen, encapsulation, decapsulation của ML-KEM. Tái tạo kết quả in sau Mã nguồn 7.2 (chapters/ch7/main.tex).
import contextlib
import io
import json
import os
import runpy
from pathlib import Path

import bo_sung_7_mlkem as kem

GOC = Path(__file__).resolve().parent.parent
ACVP = GOC / "du_lieu" / "acvp"
MA_72C = Path(__file__).resolve().parent / "ma_nguon_7_02c_hai_ham_cua_lop_ngoai_tiep.py"

# 1. keyGen: chay nguyen van vong lap cua sach (khoi ma sau Ma nguon 7.2),
#    voi json va keygen_internal duoc cap san, dung trong thu muc vector.
cwd = os.getcwd()
os.chdir(ACVP)
try:
    with contextlib.redirect_stdout(io.StringIO()):
        kq = runpy.run_path(str(MA_72C), init_globals={
            "json": json, "keygen_internal": kem.keygen_internal})
finally:
    os.chdir(cwd)
print(f"[KAT] keyGen day du: {kq['dung']}/{kq['tong']}")
print()

# 2. encapsulation (m cho truoc) va decapsulation (ca ban ma bi sua)
d = json.load(open(ACVP / "ML-KEM-encapDecap-FIPS203.internalProjection.json"))
dem = {}           # (chuc nang, bo tham so) -> [dung, tong]
ly_do = {}         # ly do -> [dung, tong]
for g in d["testGroups"]:
    ham, ten = g["function"], g["parameterSet"]
    if ham not in ("encapsulation", "decapsulation"):
        continue
    for t in g["tests"]:
        if ham == "encapsulation":
            K, c = kem.encaps_internal(bytes.fromhex(t["ek"]),
                                       bytes.fromhex(t["m"]), ten)
            ok = K.hex().upper() == t["k"] and c.hex().upper() == t["c"]
        else:
            K = kem.decaps_internal(bytes.fromhex(t["dk"]),
                                    bytes.fromhex(t["c"]), ten)
            ok = K.hex().upper() == t["k"]
            r = ly_do.setdefault(t["reason"], [0, 0])
            r[0] += ok
            r[1] += 1
        e = dem.setdefault((ham, ten), [0, 0])
        e[0] += ok
        e[1] += 1

for ten in kem.THAM_SO:
    de, en = dem[("decapsulation", ten)], dem[("encapsulation", ten)]
    print(f"{'decapsulation':<16}{ten:<13}{de[0]}/{de[1]:<9}"
          f"{'encapsulation':<16}{ten:<13}{en[0]}/{en[1]}")
print()
print("phan tich decaps theo ly do:")
for ld in sorted(ly_do):
    print(f"  {ld:<33}{ly_do[ld][0]}/{ly_do[ld][1]}")
