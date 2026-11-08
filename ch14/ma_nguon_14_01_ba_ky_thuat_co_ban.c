// Mã nguồn 14.1 - Ba kỹ thuật cơ bản của lập trình thời gian hằng: gom khác biệt bằng OR, quy về 0/1 bằng dịch bit, và chọn có điều kiện bằng mặt nạ.
// Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 14, trang 313
// Trích tự động từ chapters/ch15/main.tex (dòng 216) bằng extract.py; không sửa tay file này.

/* --- CACH SAI: thoat som ngay khi gap byte khac nhau --- */
int so_sanh_re_nhanh(const uint8_t *a, const uint8_t *b, size_t n)
{
    for (size_t i = 0; i < n; i++)
        if (a[i] != b[i])
            return 0;              /* so vong lap = so byte trung khop */
    return 1;
}

/* --- CACH DUNG: luon duyet het, gom khac biet bang OR --- */
int so_sanh_thoi_gian_hang(const uint8_t *a, const uint8_t *b, size_t n)
{
    uint8_t khac = 0;
    for (size_t i = 0; i < n; i++)
        khac |= a[i] ^ b[i];       /* khong re nhanh, khong thoat som */
    /* tra 1 khi khac == 0, van khong dung re nhanh */
    return (int)((((uint32_t)khac - 1) >> 8) & 1);
}

/* --- Chon co dieu kien bang mat na, thay cho if --- */
void chon_mat_na(uint8_t *ra, const uint8_t *x, const uint8_t *y,
                 size_t n, int dieu_kien)
{
    uint8_t m = (uint8_t)(-(int8_t)(dieu_kien & 1));   /* 0x00 hoac 0xFF */
    for (size_t i = 0; i < n; i++)
        ra[i] = (x[i] & m) | (y[i] & ~m);
}
