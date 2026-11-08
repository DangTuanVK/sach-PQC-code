# Mã nguồn 3.1 - Hệ mã hóa thu nhỏ kiểu LWE, mã hóa một bit. Các hàm phụ trợ vec, nhieu và tich sinh vector ngẫu nhiên, lấy mẫu nhiễu nhỏ và tính tích vô hướng modulo q.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 3, trang 35
# Trích tự động từ chapters/ch3/main.tex (dòng 477) bằng extract.py; không sửa tay file này.

q, n, sigma = 3329, 16, 2          # tham so do choi, KHONG an toan that

def keygen(rng):
    A = [vec(rng, n) for _ in range(n)]
    s = [nhieu(rng) for _ in range(n)]
    b = [(tich(A[i], s) + nhieu(rng)) % q for i in range(n)]
    return (A, b), s

def encrypt(pk, m, rng):
    """Ma hoa m in {0,1}. Tra ve (u, v)."""
    A, b = pk
    r = [rng.randint(0, 1) for _ in range(n)]
    u = [(sum(A[i][j]*r[i] for i in range(n)) + nhieu(rng)) % q
         for j in range(n)]
    v = (sum(b[i]*r[i] for i in range(n)) + nhieu(rng) + m*(q//2)) % q
    return (u, v)

def decrypt(sk, ct):
    u, v = ct
    x = (v - tich(u, sk)) % q
    return 1 if q//4 <= x < 3*q//4 else 0        # gan q/2 -> bit 1
