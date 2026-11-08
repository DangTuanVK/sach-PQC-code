// Mã nguồn 14.1b - (khối mã không đánh số, sau Mã nguồn 14.1)
// Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 14, trang 313
// Trích tự động từ chapters/ch15/main.tex (dòng 267) bằng extract.py; không sửa tay file này.

/* SAI: gcc -O2 co the xoa han lenh nay */
memset(khoa, 0, sizeof(khoa));

/* DUNG: buoc trinh bien dich phai thuc hien */
explicit_bzero(khoa, sizeof(khoa));           /* neu he thong ho tro */

/* hoac tu lam bang con tro volatile */
static void xoa_that(void *p, size_t n) {
    volatile uint8_t *v = (volatile uint8_t *)p;
    while (n--) *v++ = 0;
}
