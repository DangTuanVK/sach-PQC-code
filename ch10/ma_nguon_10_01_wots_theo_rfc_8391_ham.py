# Mã nguồn 10.1 - WOTS+ theo RFC 8391. Hàm xác minh không cần khóa bí mật: nó băm tiếp mỗi mảnh chữ ký cho đủ w-1 bước, sau đó so với khóa công khai.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 10, trang 255
# Trích tự động từ chapters/ch10/main.tex (dòng 2076) bằng extract.py; không sửa tay file này.

def wots_params(w):                       # RFC 8391 muc 3.1.1
    len1 = ceil(8*n / log2(w))
    len2 = floor(log2(len1 * (w-1)) / log2(w)) + 1
    return len1, len2, len1 + len2

def chain(x, start, steps, w):            # bam lap co chi so
    for i in range(start, start + steps):
        x = Hs(b"\x00", i.to_bytes(2, "big"), x)
    return x

def wots_ma_hoa(m, w):
    """Chuyen thong diep sang co so w roi noi them tong kiem."""
    len1, len2, _ = wots_params(w)
    msg  = base_w(hashlib.sha256(m).digest(), w, len1)
    csum = sum(w - 1 - x for x in msg)          # tong kiem NGUOC chieu
    csum <<= (8 - ((len2 * int(log2(w))) % 8)) % 8
    cb = csum.to_bytes(ceil(len2 * log2(w) / 8), "big")
    return msg + base_w(cb, w, len2)

def wots_sign(sk, m, w):
    d = wots_ma_hoa(m, w)
    return [chain(sk[i], 0, d[i], w) for i in range(len(d))]

def wots_verify(pk, m, sig, w):
    d = wots_ma_hoa(m, w)
    return [chain(sig[i], d[i], w-1-d[i], w) for i in range(len(d))] == pk
