# Mã nguồn 3.1b - (khối mã không đánh số, sau Mã nguồn 3.1)
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 3, trang 35
# Trích tự động từ chapters/ch3/main.tex (dòng 510) bằng extract.py; không sửa tay file này.

def tan_cong_cca(pk, sk, rng):
    m_bi_mat = rng.randint(0, 1)
    u, v = encrypt(pk, m_bi_mat, rng)         # ban ma thach thuc c*
    ct_khac = (u, (v + q//2) % q)             # dich v di q/2 -> lat bit
    m_lat = decrypt(sk, ct_khac)              # hoi tien tri: ct_khac != c*
    return m_bi_mat, 1 - m_lat                # doan cua doi thu
