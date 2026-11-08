# Mã nguồn 7.2 - Hai hàm của lớp ngoài ML-KEM. Cấu trúc bám đúng Thuật toán 17 và 18 của FIPS 203, kể cả thứ tự tính barK trước phép so sánh.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 7, trang 149
# Trích tự động từ chapters/ch7/main.tex (dòng 1562) bằng extract.py; không sửa tay file này.

def encaps_internal(ek, m, ten):
    """Thuat toan 17 (FIPS 203). Ngau nhien r DAN XUAT tu m."""
    k, eta1, eta2, du, dv = THAM_SO[ten]
    K, r = G(m + H(ek))                 # rang buoc khoa chung voi ek
    c = kpke_encrypt(ek, m, r, k, eta1, eta2, du, dv)
    return K, c

def decaps_internal(dk, c, ten):
    """Thuat toan 18 (FIPS 203). Ma hoa lai va so sanh."""
    k, eta1, eta2, du, dv = THAM_SO[ten]
    dkp = dk[:384*k]                    # khoa giai ma cua K-PKE
    ek  = dk[384*k : 768*k+32]          # khoa cong khai
    h   = dk[768*k+32 : 768*k+64]       # H(ek) da luu san
    z   = dk[768*k+64 : 768*k+96]       # gia tri tu choi ngam
    m2 = kpke_decrypt(dkp, c, k, du, dv)
    K2, r2 = G(m2 + h)
    Kbar = J(z + c)                     # khoa gia, tinh truoc
    c2 = kpke_encrypt(ek, m2, r2, k, eta1, eta2, du, dv)
    return K2 if c == c2 else Kbar      # tu choi ngam
