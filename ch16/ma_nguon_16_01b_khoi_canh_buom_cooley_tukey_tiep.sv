// Mã nguồn 16.1b - (khối mã không đánh số, sau Mã nguồn 16.1)
// Sách: Mật mã hậu lượng tử (TS. Đặng Minh Tuấn), Chương 16, trang 325
// Trích tự động từ chapters/ch16/main.tex (dòng 265) bằng extract.py; không sửa tay file này.

function automatic int mont_ref(input longint x);
    longint m, t;
    m = (x % 65536 + 65536) % 65536;   // mo phong phep lay 16 bit thap
    m = (m * 62209) % 65536;
    t = x - m * Q;
    t = t / 65536;
    return int'(t);
endfunction
