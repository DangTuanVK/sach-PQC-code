# Mã nguồn 18.1 - Phần lõi của công cụ kiểm kê chứng thư: đọc một chứng thư và tính điểm ưu tiên thay thế. Bị Shor phá, độ mạnh thấp và tuổi thọ còn dài đều nâng mức cấp bách.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 18, trang 357
# Trích tự động từ chapters/ch19/main.tex (dòng 198) bằng extract.py; không sửa tay file này.

import json, re, subprocess, sys
from collections import Counter
from datetime import datetime

OPENSSL = "openssl"                 # OpenSSL 3.5 tro len (doc duoc ML-DSA)
PHAN_LOAI = {                       # thuat toan -> (ho, tinh trang)
    "rsaEncryption":  ("RSA",    "PHA VO boi Shor"),
    "id-ecPublicKey": ("ECC",    "PHA VO boi Shor"),
    "ED25519":        ("EdDSA",  "PHA VO boi Shor"),
    "ML-DSA-65":      ("ML-DSA", "an toan hau luong tu"),
}

def doc_chung_thu(pem):
    """Tra ve (thuat toan, so bit, ngay het han) cua mot chung thu."""
    r = subprocess.run([OPENSSL, "x509", "-noout", "-text", "-enddate"],
                       input=pem, stdout=subprocess.PIPE,
                       universal_newlines=True, check=True)
    t = r.stdout
    alg = re.search(r"Public Key Algorithm: (\S+)", t).group(1)
    # ML-DSA va Ed25519 khong in "(... bit)" -> ghi so bit la 0
    m = re.search(r"Public-Key: \((\d+) bit\)", t)
    bits = int(m.group(1)) if m else 0
    het = re.search(r"notAfter=(.+)", t).group(1).strip()
    return alg, bits, datetime.strptime(het, "%b %d %H:%M:%S %Y %Z")

def diem_uu_tien(ho, bits, nam_con_lai):
    """Diem cang cao cang can thay som."""
    if ho in ("ML-DSA", "SLH-DSA"):
        return 0                          # da an toan
    d = 50                                # bi Shor pha
    if ho == "RSA":                       # nguong do manh chi ap cho RSA
        d += 25 if bits <= 2048 else (10 if bits <= 3072 else 0)
    return d + min(max(int(nam_con_lai), 0), 25)  # song cang lau -> cang gap
