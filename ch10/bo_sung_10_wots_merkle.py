# Không có trong sách: các dòng import, hai hàm phụ Hs, base_w và phần chạy thử WOTS+ cùng cây Merkle h = 4. Tái tạo kết quả in sau Mã nguồn 10.1 (chapters/ch10/main.tex).
import hashlib
import random
from math import ceil, floor, log2

import ma_nguon_10_01_wots_theo_rfc_8391_ham as wots
import ma_nguon_10_01b_wots_theo_rfc_8391_ham_tiep as merkle

n = 32                      # do dai gia tri bam (byte)


def Hs(*phan):
    """SHA-256 cua phan ghep noi cac doi so."""
    return hashlib.sha256(b"".join(phan)).digest()


def base_w(X, w, out_len):
    """RFC 8391 muc 2.6: tach chuoi byte X thanh out_len chu so co so w."""
    lg = int(log2(w))
    vao, total, bits, ra = 0, 0, 0, []
    for _ in range(out_len):
        if bits == 0:
            total = X[vao]
            vao += 1
            bits = 8
        bits -= lg
        ra.append((total >> bits) & (w - 1))
    return ra


# Gan vao cac module cua sach (cac dong import va ham phu bi luoc bo)
wots.hashlib, wots.ceil, wots.floor, wots.log2 = hashlib, ceil, floor, log2
wots.n, wots.Hs, wots.base_w = n, Hs, base_w
merkle.Hs = Hs

rng = random.Random(2026)   # sach khong neu hat giong


def wots_keygen(w):
    _, _, L = wots.wots_params(w)
    sk = [rng.randbytes(n) for _ in range(L)]
    pk = [wots.chain(x, 0, w - 1, w) for x in sk]
    return sk, pk


w = 16
sk, pk = wots_keygen(w)
m = b"firmware v1.0"
sig = wots.wots_sign(sk, m, w)
print(f"=== WOTS+ ky va xac minh (w={w}) ===")
print(f"  chu ky hop le      : {wots.wots_verify(pk, m, sig, w)}")
print(f"  thong diep khac    : {wots.wots_verify(pk, b'firmware v1.1', sig, w)}")
print(f"  kich thuoc chu ky  : {sum(len(s) for s in sig)} byte")
print()

# Cay Merkle: moi la la gia tri bam cua mot khoa cong khai WOTS+
h = 4
khoa = [wots_keygen(w) for _ in range(2**h)]
la = [Hs(*pk_i) for _, pk_i in khoa]
tang = merkle.merkle_build(la)
goc = tang[-1][0]


def duong_xac_thuc(tang, idx):
    duong = []
    for muc in tang[:-1]:
        duong.append(muc[idx ^ 1])          # nut anh em
        idx >>= 1
    return duong


dung = 0
for idx in range(2**h):
    duong = duong_xac_thuc(tang, idx)
    dung += (merkle.merkle_root_tu_path(la[idx], idx, duong) == goc)
print("=== Cay Merkle ===")
print(f"  chieu cao h = {h}, so khoa mot lan = {2**h}")
print(f"  duong xac thuc dung cho {dung}/{2**h} chi so, moi duong dai {len(duong)} nut"
      f" = {sum(len(s) for s in duong)} byte")
