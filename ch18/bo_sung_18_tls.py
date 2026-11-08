# Không có trong sách: chạy tự động các lệnh của Mã nguồn 18.1 (bắt tay TLS 1.3 lai). Tái tạo kết quả in sau Mã nguồn 18.1 (chapters/ch18/main.tex).
# Can OpenSSL 3.5 tro len tren PATH. Chay cac buoc 2-4 cua Ma nguon 18.1 trong mot thu muc tam:
# tao chung thu ML-DSA-65, dung may chu ep nhom X25519MLKEM768, roi cho may khach ket noi.
import re
import socket
import subprocess
import tempfile
import time

def cong_trong():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]

with tempfile.TemporaryDirectory() as tmp:
    subprocess.run(["openssl", "req", "-x509", "-newkey", "ML-DSA-65",
                    "-keyout", "key_dsa.pem", "-out", "cert_dsa.pem", "-days", "30",
                    "-nodes", "-subj", "/CN=pqc-dsa"],
                   cwd=tmp, check=True, capture_output=True)
    cong = str(cong_trong())
    may_chu = subprocess.Popen(["openssl", "s_server", "-cert", "cert_dsa.pem",
                                "-key", "key_dsa.pem", "-accept", cong,
                                "-groups", "X25519MLKEM768", "-tls1_3"],
                               cwd=tmp, stdin=subprocess.PIPE,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(50):                     # cho may chu san sang
            time.sleep(0.2)
            if may_chu.poll() is not None:
                raise SystemExit("may chu openssl dung som")
            try:
                socket.create_connection(("127.0.0.1", int(cong)), 0.2).close()
                break
            except OSError:
                pass
        kq = subprocess.run(["openssl", "s_client", "-connect", "localhost:" + cong,
                             "-groups", "X25519MLKEM768", "-tls1_3"],
                            input="Q\n", capture_output=True, text=True, timeout=30)
    finally:
        may_chu.kill()
        may_chu.wait()

for dong in kq.stdout.splitlines():
    if re.search(r"group|handshake has read", dong):
        print(dong)
