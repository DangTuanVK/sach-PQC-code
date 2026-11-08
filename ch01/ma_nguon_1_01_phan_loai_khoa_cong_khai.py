# Mã nguồn 1.1 - Phân loại khóa công khai trong một chứng thư X.509 theo mức độ tổn thương trước thuật toán Shor.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 1, trang 9
# Trích tự động từ chapters/ch1/main.tex (dòng 351) bằng extract.py; không sửa tay file này.

from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa, ec, dsa, ed25519

# Độ mạnh cổ điển (bit): NIST SP 800-57 Phần 1, SP 800-56B Rev.2 (RSA-4096).
DO_MANH_EC = {"secp256r1": 128, "secp384r1": 192, "secp521r1": 256}

def phan_loai(khoa_cong_khai):
    """Trả về (họ thuật toán, độ mạnh cổ điển tính bằng bit, tình trạng)."""
    if isinstance(khoa_cong_khai, rsa.RSAPublicKey):
        n = khoa_cong_khai.key_size
        do_manh = {2048: 112, 3072: 128, 4096: 152, 7680: 192}.get(n)
        return f"RSA-{n}", do_manh, "PHA VO boi Shor"
    if isinstance(khoa_cong_khai, ec.EllipticCurvePublicKey):
        ten = khoa_cong_khai.curve.name
        return f"ECC-{ten}", DO_MANH_EC.get(ten), "PHA VO boi Shor"
    if isinstance(khoa_cong_khai, dsa.DSAPublicKey):
        return f"DSA-{khoa_cong_khai.key_size}", None, "PHA VO boi Shor"
    if isinstance(khoa_cong_khai, ed25519.Ed25519PublicKey):
        return "Ed25519", 128, "PHA VO boi Shor"
    return type(khoa_cong_khai).__name__, None, "chua phan loai"

def quet_chung_thu(duong_dan):
    with open(duong_dan, "rb") as f:
        cert = x509.load_pem_x509_certificate(f.read())
    ho, do_manh, tinh_trang = phan_loai(cert.public_key())
    print(f"{duong_dan}")
    print(f"  chu the    : {cert.subject.rfc4514_string()}")
    print(f"  thuat toan : {ho}  (~{do_manh} bit co dien)")
    print(f"  het han    : {cert.not_valid_after_utc:%Y-%m-%d}")
    print(f"  tinh trang : {tinh_trang}")
