# Mã nguồn 12.1 - Mã Reed-Muller bậc một với giải mã hợp lý cực đại. Đỉnh lớn nhất của biến đổi Hadamard xác định trực tiếp từ mã gần nhất.
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 12, trang 281
# Trích tự động từ chapters/ch13/main.tex (dòng 256) bằng extract.py; không sửa tay file này.

class RM1:
    def __init__(self, m):
        self.m, self.N, self.K = m, 1 << m, m + 1

    def encode(self, msg):
        """msg: m+1 bit. Tu ma = ham tuyen tinh danh gia tren F_2^m."""
        b0, b = msg[0], msg[1:]
        return [b0 ^ sum(b[i] for i in range(self.m) if (x >> i) & 1) % 2
                for x in range(self.N)]

    def decode(self, y):
        """Giai ma hop ly cuc dai bang bien doi Hadamard nhanh: O(N log N)."""
        t = [1 - 2*b for b in y]                  # 0/1 -> +1/-1
        h = 1
        while h < self.N:                          # bien doi tai cho
            for i in range(0, self.N, h*2):
                for j in range(i, i + h):
                    a, b = t[j], t[j + h]
                    t[j], t[j + h] = a + b, a - b
            h *= 2
        idx = max(range(self.N), key=lambda i: abs(t[i]))   # dinh lon nhat
        b0 = 0 if t[idx] > 0 else 1
        return [b0] + [(idx >> i) & 1 for i in range(self.m)]
