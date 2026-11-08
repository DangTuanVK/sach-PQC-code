# Mã nguồn 8.1 - Vòng lặp ký của ML-DSA. Mỗi điểm continue gom hai trong bốn phép kiểm loại bỏ; chỉ khi vượt qua cả bốn thì chữ ký mới được xuất ra.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 8, trang 193
# Trích tự động từ chapters/ch8/main.tex (dòng 2177) bằng extract.py; không sửa tay file này.

def sign_internal(sk, Mp, rnd, ten):
    k, l, eta, tau, lam, g1, g2, om = THAM_SO[ten]
    beta = tau * eta                       # chan tren cua ||c*s||_inf
    rho, K, tr, s1, s2, t0 = sk_decode(sk, k, l, eta)
    s1h, s2h, t0h = ntt_vec(s1), ntt_vec(s2), ntt_vec(t0)
    A  = expand_A(rho, k, l)
    mu    = H(tr + Mp, 64)                 # dai dien thong diep
    rhopp = H(K + rnd + mu, 64)            # mam bi mat cho mat na
    kappa = 0
    while True:
        y  = expand_mask(rhopp, kappa, l, g1)          # mat na moi
        w  = [intt(sum_pmul(A[i], ntt_vec(y))) for i in range(k)]
        w1 = [[high_bits(x, g2) for x in p] for p in w]  # cam ket
        ctil = H(mu + w1_encode(w1, k, g2), lam // 4)    # bam cam ket
        c    = sample_in_ball(ctil, tau, lam)            # thach thuc
        ch   = ntt(c)
        cs1 = [intt(pmul(ch, s1h[i])) for i in range(l)]
        cs2 = [intt(pmul(ch, s2h[i])) for i in range(k)]
        z  = [padd(y[i], cs1[i]) for i in range(l)]      # phan hoi
        r0 = [[low_bits(x, g2) for x in psub(w[i], cs2[i])] for i in range(k)]
        if inf_norm(z) >= g1 - beta or inf_norm(r0) >= g2 - beta:
            kappa += l; continue                         # LOAI BO
        ct0 = [intt(pmul(ch, t0h[i])) for i in range(k)]
        h = make_hint_vec(ct0, w, cs2, g2)
        if inf_norm(ct0) >= g2 or sum(sum(p) for p in h) > om:
            kappa += l; continue                         # LOAI BO
        return sig_encode(ctil, z, h, k, l, om, g1)
