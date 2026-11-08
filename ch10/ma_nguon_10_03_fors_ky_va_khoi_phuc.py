# Mã nguồn 10.3 - FORS: ký và khôi phục khóa công khai từ chữ ký. Người xác minh dựng lại khóa công khai FORS, sau đó kiểm tra nó khớp với giá trị mà siêu cây đã ký.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 10, trang 258
# Trích tự động từ chapters/ch10/main.tex (dòng 2208) bằng extract.py; không sửa tay file này.

def fors_sign(self, chi_so, dia_chi):
    """chi_so: k chi so, moi cai a bit -- lay tu ban bam thong diep."""
    sig = []
    for i, idx in enumerate(chi_so):
        la = [Hs(b"L", self.fors_la(i, j, dia_chi))
              for j in range(1 << self.a)]          # dung cay thu i
        duong, cur, lop = [], idx, la
        while len(lop) > 1:
            duong.append(lop[cur ^ 1])              # nut anh em
            lop = [Hs(lop[t], lop[t+1]) for t in range(0, len(lop), 2)]
            cur >>= 1
        sig.append((self.fors_la(i, idx, dia_chi), duong))
    return sig

def fors_pk_tu_sig(self, chi_so, sig):
    """Khoi phuc khoa cong khai FORS tu chu ky -- khong can khoa bi mat."""
    goc = []
    for (bi_mat, duong), idx in zip(sig, chi_so):
        x, cur = Hs(b"L", bi_mat), idx
        for s in duong:
            x = Hs(x, s) if cur % 2 == 0 else Hs(s, x)
            cur >>= 1
        goc.append(x)
    return Hs(b"P", *goc)
