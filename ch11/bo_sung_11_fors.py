# Không có trong sách: khung lớp FORS (tham số, fors_la, Hs) và phần chạy thử với n = 16, a = 4, k = 8. Tái tạo kết quả in sau Mã nguồn 11.2 (chapters/ch11/main.tex).
import hashlib

import ma_nguon_11_02_fors_ky_va_khoi_phuc as mn

N = 16                      # do dai gia tri bam (byte)


def Hs(*phan):
    """SHA-256 cua phan ghep noi cac doi so, cat con n byte."""
    return hashlib.sha256(b"".join(phan)).digest()[:N]


mn.Hs = Hs                  # hai ham cua sach goi Hs o muc module


class FORS:
    """Khung lop toi thieu: tham so a, k, n va ham sinh phan tu bi mat."""

    def __init__(self, sk_seed, n=N, a=4, k=8):
        self.sk_seed, self.n, self.a, self.k = sk_seed, n, a, k

    def fors_la(self, i, j, dia_chi):
        """Phan tu bi mat thu j cua cay thu i (PRF tu hat giong bi mat)."""
        return Hs(b"S", self.sk_seed, dia_chi,
                  i.to_bytes(4, "big"), j.to_bytes(4, "big"))

    def chi_so(self, m):
        """Lay k chi so, moi chi so a bit, tu ban bam thong diep."""
        x = int.from_bytes(hashlib.sha256(m).digest(), "big")
        return [(x >> (self.a * i)) & ((1 << self.a) - 1) for i in range(self.k)]

    def fors_pk(self, dia_chi):
        """Khoa cong khai FORS dung truc tiep tu khoa bi mat."""
        goc = []
        for i in range(self.k):
            lop = [Hs(b"L", self.fors_la(i, j, dia_chi)) for j in range(1 << self.a)]
            while len(lop) > 1:
                lop = [Hs(lop[t], lop[t+1]) for t in range(0, len(lop), 2)]
            goc.append(lop[0])
        return Hs(b"P", *goc)

    fors_sign = mn.fors_sign
    fors_pk_tu_sig = mn.fors_pk_tu_sig


f = FORS(sk_seed=bytes(range(N)))
dia_chi = b"\x00" * 8
pk = f.fors_pk(dia_chi)
m = b"thong diep can ky"
sig = f.fors_sign(f.chi_so(m), dia_chi)
print(f"  chu ky FORS hop le  : {f.fors_pk_tu_sig(f.chi_so(m), sig) == pk}")
print(f"  thong diep khac     : {f.fors_pk_tu_sig(f.chi_so(b'thong diep khac'), sig) == pk}")
kich_thuoc = sum(len(bi_mat) + sum(len(s) for s in duong) for bi_mat, duong in sig)
print(f"  kich thuoc phan FORS: {kich_thuoc} byte")
