// Mã nguồn 6.1a - (khối mã không đánh số, đứng trước Mã nguồn 6.1)
// Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 6, trang 119
// Trích tự động từ chapters/ch6/main.tex (dòng 1903) bằng extract.py; không sửa tay file này.

#define KYBER_Q     3329
#define QINV      62209        /* q^{-1} mod 2^16 */

/* Rut gon Montgomery: tra ve a * R^{-1} mod q, voi R = 2^16 */
static int16_t montgomery_reduce(int32_t a) {
    int16_t t = (int16_t)a * QINV;        /* ep kieu: giu 16 bit thap */
    return (a - (int32_t)t * KYBER_Q) >> 16;
}

/* Mot khoi buom Cooley-Tukey */
static void butterfly(int16_t *f, int j, int len, int16_t zeta) {
    int16_t t = montgomery_reduce((int32_t)zeta * f[j + len]);
    f[j + len] = f[j] - t;
    f[j]       = f[j] + t;
}
