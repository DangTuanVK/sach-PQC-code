# Mã nguồn 17.1 - Mô phỏng tấn công CPA. Tham số mask bật chế độ che mặt nạ bậc một: bí mật được chia thành hai phần và cả hai đều rò rỉ.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 17, trang 336
# Trích tự động từ chapters/ch17/main.tex (dòng 222) bằng extract.py; không sửa tay file này.

def sinh_vet(s_that, a_list, sigma, rng, mask=False):
    """Vet ro ri = trong so Hamming cua tich + nhieu Gauss."""
    vet = []
    for a in a_list:
        if mask:
            s1 = rng.randrange(q)              # chia bi mat thanh 2 phan
            s2 = (s_that - s1) % q
            l = hw(a*s1 % q) + hw(a*s2 % q)    # ro ri cua CA HAI phan
        else:
            l = hw(a*s_that % q)
        vet.append(l + rng.gauss(0, sigma))
    return vet

def cpa(a_list, vet):
    """Voi moi gia tri doan, tinh tuong quan giua mo hinh va vet do."""
    tq = []
    for g in range(q):                          # duyet het khong gian doan
        mo_hinh = [hw(a*g % q) for a in a_list]
        tq.append((abs(pearson(mo_hinh, vet)), g))
    tq.sort(reverse=True)
    return tq                                   # xep hang theo tuong quan
