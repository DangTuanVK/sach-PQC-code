# Mã nguồn 16.1b - (khối mã không đánh số, sau Mã nguồn 16.1)
# Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 16, trang 334
# Trích tự động từ chapters/ch17/main.tex (dòng 253) bằng extract.py; không sửa tay file này.

def pearson(x, y):
    n = len(x); mx = mean(x); my = mean(y)
    sxy = sum((a-mx)*(b-my) for a, b in zip(x, y))
    sx  = math.sqrt(sum((a-mx)**2 for a in x))
    sy  = math.sqrt(sum((b-my)**2 for b in y))
    return sxy/(sx*sy) if sx and sy else 0.0
