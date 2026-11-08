# Mã nguồn 18.1 - Dựng bắt tay TLS 1.3 hậu lượng tử hoàn toàn bằng OpenSSL: nhóm khóa lai cộng chứng thư ML-DSA.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 18, trang 349
# Trích tự động từ chapters/ch18/main.tex (dòng 282) bằng extract.py; không sửa tay file này.

# 1. Tao chung thu tu ky, khoa ECDSA P-256
openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:P-256 \
    -keyout key.pem -out cert.pem -days 30 -nodes -subj "/CN=pqc-demo"

# 2. Tao chung thu voi khoa ML-DSA-65 (OpenSSL 3.5 tro len)
openssl req -x509 -newkey ML-DSA-65 \
    -keyout key_dsa.pem -out cert_dsa.pem -days 30 -nodes -subj "/CN=pqc-dsa"

# 3. May chu, ep dung nhom lai
openssl s_server -cert cert_dsa.pem -key key_dsa.pem \
    -accept 4433 -groups X25519MLKEM768 -tls1_3

# 4. May khach, in ra nhom da thuong luong va so byte bat tay
echo Q | openssl s_client -connect localhost:4433 \
    -groups X25519MLKEM768 -tls1_3 | grep -E "group|handshake has read"
