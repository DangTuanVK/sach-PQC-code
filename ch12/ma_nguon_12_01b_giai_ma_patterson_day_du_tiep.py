# Mã nguồn 12.1b - (khối mã không đánh số, sau Mã nguồn 12.1)
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 12, trang 273
# Trích tự động từ chapters/ch12/main.tex (dòng 320) bằng extract.py; không sửa tay file này.

def _bat_kha_quy(self, g):
    """g bat kha quy tren GF(2^m) <=> gcd(z^(q^i) - z, g) = 1
       voi moi i = 1..deg(g)/2, trong do q = 2^m.
       LUU Y: Frobenius o day la x -> x^q, KHONG phai x -> x^2."""
    F = self.F
    if any(p_eval(F, g, a) == 0 for a in range(F.n)):
        return False
    x = [0, 1]
    for _ in range(p_deg(g) // 2):
        for _ in range(F.m):               # x -> x^(2^m) = x^q
            x = p_mod(F, p_mul(F, x, x), g)
        d, _, _ = p_egcd(F, p_add(x, [0, 1]), g)
        if p_deg(d) > 0:
            return False
    return True
