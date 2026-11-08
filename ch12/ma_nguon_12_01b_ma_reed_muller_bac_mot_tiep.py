# Mã nguồn 12.1b - (khối mã không đánh số, sau Mã nguồn 12.1)
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 12, trang 281
# Trích tự động từ chapters/ch13/main.tex (dòng 309) bằng extract.py; không sửa tay file này.

def decode(self, y):
    """Cong don cac ban sao truoc khi bien doi Hadamard."""
    N = self.rm.N
    cong = [0]*N
    for r in range(self.mul):
        for i in range(N):
            cong[i] += 1 - 2*y[r*N + i]      # cong theo mien +1/-1
    # ... phan con lai giong RM1.decode
