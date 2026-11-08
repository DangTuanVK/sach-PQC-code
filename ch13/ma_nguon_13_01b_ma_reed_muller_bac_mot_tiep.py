# Mã nguồn 13.1b - (khối mã không đánh số, sau Mã nguồn 13.1)
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 13, trang 283
# Trích tự động từ chapters/ch13/main.tex (dòng 309) bằng extract.py; không sửa tay file này.

def decode(self, y):
    """Cong don cac ban sao truoc khi bien doi Hadamard."""
    N = self.rm.N
    cong = [0]*N
    for r in range(self.mul):
        for i in range(N):
            cong[i] += 1 - 2*y[r*N + i]      # cong theo mien +1/-1
    # ... phan con lai giong RM1.decode
