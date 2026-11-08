# Mã nguồn 1.1b - (khối mã không đánh số, sau Mã nguồn 1.1)
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 1, trang 9
# Trích tự động từ chapters/ch1/main.tex (dòng 405) bằng extract.py; không sửa tay file này.

import socket, ssl
from cryptography import x509

def lay_chung_thu_tls(host, port=443):
    ctx = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=5) as sock:
        with ctx.wrap_socket(sock, server_hostname=host) as tls:
            der = tls.getpeercert(binary_form=True)
            print("  bo ma TLS :", tls.cipher()[0])
            return x509.load_der_x509_certificate(der)
