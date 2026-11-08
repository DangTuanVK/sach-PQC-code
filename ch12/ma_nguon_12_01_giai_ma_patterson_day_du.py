# Mã nguồn 12.1 - Giải mã Patterson đầy đủ, bám đúng sáu bước ở Hình 12.2.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 12, trang 273
# Trích tự động từ chapters/ch12/main.tex (dòng 289) bằng extract.py; không sửa tay file này.

def patterson(self, c):
    F, g, L, t = self.F, self.g, self.L, self.t
    S = [0]                                     # 1. hoi chung
    for j, a in enumerate(L):
        if c[j]:
            S = p_add(S, p_inv_mod(F, p_mod(F, p_add([a], [0, 1]), g), g))
    if not any(S):
        return [0]*self.n                       # khong co loi
    T  = p_inv_mod(F, S, g)                     # 2. nghich dao
    Tz = p_add(T, [0, 1])                       #    T(z) + z
    if not any(Tz):
        sigma = [0, 1]
    else:
        R = p_sqrt_mod(F, Tz, g)                # 3. can bac hai
        a_, b_ = self._eea_dung_som(R, g, t//2) # 4. Euclid dung som
        sigma = p_add(p_mul(F, a_, a_),         # 5. sigma = a^2 + z b^2
                      p_mul(F, [0, 1], p_mul(F, b_, b_)))
    return [1 if p_eval(F, sigma, x) == 0 else 0 for x in L]   # 6. nghiem
