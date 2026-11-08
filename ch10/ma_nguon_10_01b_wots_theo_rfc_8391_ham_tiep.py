# Mã nguồn 10.1b - (khối mã không đánh số, sau Mã nguồn 10.1)
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 10, trang 239
# Trích tự động từ chapters/ch10/main.tex (dòng 1103) bằng extract.py; không sửa tay file này.

def merkle_build(la):
    tang = [list(la)]
    while len(tang[-1]) > 1:
        tr = tang[-1]
        tang.append([Hs(tr[i], tr[i+1]) for i in range(0, len(tr), 2)])
    return tang

def merkle_root_tu_path(la, idx, duong):
    x = la
    for s in duong:
        x = Hs(x, s) if idx % 2 == 0 else Hs(s, x)   # trai hay phai
        idx >>= 1
    return x
