# Báo cáo chạy mã nguồn của sách "Mật mã hậu lượng tử"

Python 3.11.18; 46 khối mã: CHẠY ĐƯỢC 30, CHỈ ĐỊNH NGHĨA 6, KHÔNG CHẠY 6, KHỚP SÁCH 2, LỆCH SÁCH 1, TRÍCH ĐOẠN 1.

Trạng thái: **KHỚP SÁCH** (chạy được và kết quả trùng với "Kết quả chạy" in trong sách), **CHẠY ĐƯỢC** (sách không in kết quả), **TRÍCH ĐOẠN** (khối mã trích từ một cài đặt lớn hơn, gọi hàm phụ trợ không in trong sách nên không chạy độc lập), **CHỈ ĐỊNH NGHĨA** (khối chỉ định nghĩa hàm, chạy không lỗi nhưng không in gì; "Kết quả chạy" in trong sách đến từ phần gọi thử không in trong sách), **KHÔNG CHẠY** (mã C, SystemVerilog, bash: không chạy tự động), **LỆCH SÁCH**, **LỖI**, **TIMEOUT**.

| Mã nguồn | Trang | Nội dung | Trạng thái | Thời gian | Kết quả |
|---|---|---|---|---|---|
| 1.1 | 9 | Phân loại khóa công khai trong một chứng thư X.509 theo mức độ tổn thương trước thuật toán Shor. | CHẠY ĐƯỢC | 0.1 s | [ma_nguon_1_01.txt](ch01/ma_nguon_1_01.txt) |
| 1.1b | 9 | (khối mã không đánh số, sau Mã nguồn 1.1) | CHẠY ĐƯỢC | 0.1 s | [ma_nguon_1_01b.txt](ch01/ma_nguon_1_01b.txt) |
| 2.1 | 21 | Phần lượng tử của mô phỏng Shor: chọn q, dựng phổ sau QFT và lấy mẫu kết quả đo. | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_2_01.txt](ch02/ma_nguon_2_01.txt) |
| 2.2 | 22 | Vòng lặp chính của mô phỏng Shor, dùng các hàm ở Mã nguồn 2.1; vòng lặp cuối in kết quả cho N = 15, 21, 35. | KHỚP SÁCH | 0.1 s | [ma_nguon_2_02.txt](ch02/ma_nguon_2_02.txt) |
| 3.1 | 35 | Hệ mã hóa thu nhỏ kiểu LWE, mã hóa một bit. Các hàm phụ trợ vec, nhieu và tich sinh vector ngẫu nhiên, lấy mẫu nhiễu nhỏ và tính tích vô hướng modulo q. | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_3_01.txt](ch03/ma_nguon_3_01.txt) |
| 3.1b | 35 | (khối mã không đánh số, sau Mã nguồn 3.1) | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_3_01b.txt](ch03/ma_nguon_3_01b.txt) |
| 3.2 | 36 | Bọc biến đổi FO quanh hệ mã hóa của Mã nguồn 3.1, mô phỏng cấu trúc của Thuật toán 17 và 18 trong FIPS 203. Hàm G là SHA3-512, hàm H là SHA3-256 (dùng thay cho J), bam_ct băm bản mã. | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_3_02.txt](ch03/ma_nguon_3_02.txt) |
| 3.2b | 36 | (khối mã không đánh số, sau Mã nguồn 3.2) | CHỈ ĐỊNH NGHĨA | 0.0 s | [ma_nguon_3_02b.txt](ch03/ma_nguon_3_02b.txt) |
| 4.1 | 45 | Tính kích thước khóa và bản mã trực tiếp từ công thức trong văn bản chuẩn, sau đó đối chiếu với bảng công bố. | LỆCH SÁCH | 0.0 s | [ma_nguon_4_01.txt](ch04/ma_nguon_4_01.txt) |
| 5.1 | 78 | Thuật toán LLL. Cơ sở luôn giữ hệ số nguyên; chỉ phần trực giao hóa dùng số thực. | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_5_01.txt](ch05/ma_nguon_5_01.txt) |
| 5.1b | 78 | (khối mã không đánh số, sau Mã nguồn 5.1) | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_5_01b.txt](ch05/ma_nguon_5_01b.txt) |
| 6.1a | 119 | (khối mã không đánh số, đứng trước Mã nguồn 6.1) | KHÔNG CHẠY | 0.0 s | [ma_nguon_6_01a_doan_ma_mo_dau.c](../ch06/ma_nguon_6_01a_doan_ma_mo_dau.c) |
| 6.1 | 119 | NTT và INTT chung cho ML-KEM và ML-DSA. Cùng một hàm: khi gọi với KEM, hàm trùng Thuật toán 9, 10 của FIPS 203; khi gọi với DSA, hàm trùng Thuật toán 41, 42 của FIPS 204. | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_6_01.txt](ch06/ma_nguon_6_01.txt) |
| 6.2 | 118 | Phép nhân trong miền NTT của hai chuẩn: 128 phép nhân cơ sở cho ML-KEM, 256 phép nhân từng phần tử cho ML-DSA. | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_6_02.txt](ch06/ma_nguon_6_02.txt) |
| 6.3 | 120 | Phép nhân trực tiếp trong Z_q[X]/(X^256+1), dùng làm chuẩn đối chiếu cho NTT. | CHỈ ĐỊNH NGHĨA | 0.0 s | [ma_nguon_6_03.txt](ch06/ma_nguon_6_03.txt) |
| 7.1 | 147 | Tính cận 7.13 cho tỉ lệ giải mã sai của ba bộ tham số. Chương trình cần NumPy và chạy khoảng một phút. | CHẠY ĐƯỢC | 54.5 s | [ma_nguon_7_01.txt](ch07/ma_nguon_7_01.txt) |
| 7.2 | 149 | Hai hàm của lớp ngoài ML-KEM. Cấu trúc bám đúng Thuật toán 17 và 18 của FIPS 203, kể cả thứ tự tính barK trước phép so sánh. | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_7_02.txt](ch07/ma_nguon_7_02.txt) |
| 7.2b | 149 | (khối mã không đánh số, sau Mã nguồn 7.2) | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_7_02b.txt](ch07/ma_nguon_7_02b.txt) |
| 7.2c | 149 | (khối mã không đánh số, sau Mã nguồn 7.2) | TRÍCH ĐOẠN | 0.0 s | [ma_nguon_7_02c.txt](ch07/ma_nguon_7_02c.txt) |
| 8.1 | 193 | Vòng lặp ký của ML-DSA. Mỗi điểm continue gom hai trong bốn phép kiểm loại bỏ; chỉ khi vượt qua cả bốn thì chữ ký mới được xuất ra. | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_8_01.txt](ch08/ma_nguon_8_01.txt) |
| 9.1 | 215 | Bộ lấy mẫu Gauss rời rạc bằng bảng CDT. Vòng lặp trong lay_mau_ct luôn chạy đủ 2T+1 bước bất kể giá trị lấy được. | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_9_01.txt](ch09/ma_nguon_9_01.txt) |
| 9.2 | 216 | Bộ lấy mẫu CDT thoát sớm. Kết quả thống kê giống Mã nguồn 9.1, nhưng số vòng lặp phụ thuộc giá trị trả về. | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_9_02.txt](ch09/ma_nguon_9_02.txt) |
| 10.1 | 239 | WOTS+ theo RFC 8391. Hàm xác minh không cần khóa bí mật: nó băm tiếp mỗi mảnh chữ ký cho đủ w-1 bước, sau đó so với khóa công khai. | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_10_01.txt](ch10/ma_nguon_10_01.txt) |
| 10.1b | 239 | (khối mã không đánh số, sau Mã nguồn 10.1) | CHỈ ĐỊNH NGHĨA | 0.0 s | [ma_nguon_10_01b.txt](ch10/ma_nguon_10_01b.txt) |
| 11.1 | 261 | Tính kích thước chữ ký SLH-DSA từ công thức trong đặc tả, sau đó đối chiếu với bảng tham số công bố. | KHỚP SÁCH | 0.0 s | [ma_nguon_11_01.txt](ch11/ma_nguon_11_01.txt) |
| 11.2 | 262 | FORS: ký và khôi phục khóa công khai từ chữ ký. Người xác minh dựng lại khóa công khai FORS, sau đó kiểm tra nó khớp với giá trị mà siêu cây đã ký. | CHỈ ĐỊNH NGHĨA | 0.0 s | [ma_nguon_11_02.txt](ch11/ma_nguon_11_02.txt) |
| 12.1 | 273 | Giải mã Patterson đầy đủ, bám đúng sáu bước ở Hình 12.2. | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_12_01.txt](ch12/ma_nguon_12_01.txt) |
| 12.1b | 273 | (khối mã không đánh số, sau Mã nguồn 12.1) | CHỈ ĐỊNH NGHĨA | 0.0 s | [ma_nguon_12_01b.txt](ch12/ma_nguon_12_01b.txt) |
| 12.1c | 273 | (khối mã không đánh số, sau Mã nguồn 12.1) | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_12_01c.txt](ch12/ma_nguon_12_01c.txt) |
| 13.1 | 283 | Mã Reed-Muller bậc một với giải mã hợp lý cực đại. Đỉnh lớn nhất của biến đổi Hadamard xác định trực tiếp từ mã gần nhất. | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_13_01.txt](ch13/ma_nguon_13_01.txt) |
| 13.1b | 283 | (khối mã không đánh số, sau Mã nguồn 13.1) | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_13_01b.txt](ch13/ma_nguon_13_01b.txt) |
| 14.1 | 305 | Thuật toán ký của UOV. Toàn bộ độ khó nằm ở việc đối thủ không biết không gian dầu T^-1(O); khi biết nó, việc ký chỉ còn là khử Gauss. | CHỈ ĐỊNH NGHĨA | 0.0 s | [ma_nguon_14_01.txt](ch14/ma_nguon_14_01.txt) |
| 15.1 | 315 | Ba kỹ thuật cơ bản của lập trình thời gian hằng: gom khác biệt bằng OR, quy về 0/1 bằng dịch bit, và chọn có điều kiện bằng mặt nạ. | KHÔNG CHẠY | 0.0 s | [ma_nguon_15_01_ba_ky_thuat_co_ban.c](../ch15/ma_nguon_15_01_ba_ky_thuat_co_ban.c) |
| 15.1b | 315 | (khối mã không đánh số, sau Mã nguồn 15.1) | KHÔNG CHẠY | 0.0 s | [ma_nguon_15_01b_ba_ky_thuat_co_ban_tiep.c](../ch15/ma_nguon_15_01b_ba_ky_thuat_co_ban_tiep.c) |
| 16.1 | 325 | Khối cánh bướm Cooley-Tukey với rút gọn Montgomery, viết bằng SystemVerilog. Ba tầng đường ống tách phép nhân, phép rút gọn và phép cộng/trừ. | KHÔNG CHẠY | 0.0 s | [ma_nguon_16_01_khoi_canh_buom_cooley_tukey.sv](../ch16/ma_nguon_16_01_khoi_canh_buom_cooley_tukey.sv) |
| 16.1b | 325 | (khối mã không đánh số, sau Mã nguồn 16.1) | KHÔNG CHẠY | 0.0 s | [ma_nguon_16_01b_khoi_canh_buom_cooley_tukey_tiep.sv](../ch16/ma_nguon_16_01b_khoi_canh_buom_cooley_tukey_tiep.sv) |
| 17.1 | 336 | Mô phỏng tấn công CPA. Tham số mask bật chế độ che mặt nạ bậc một: bí mật được chia thành hai phần và cả hai đều rò rỉ. | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_17_01.txt](ch17/ma_nguon_17_01.txt) |
| 17.1b | 336 | (khối mã không đánh số, sau Mã nguồn 17.1) | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_17_01b.txt](ch17/ma_nguon_17_01b.txt) |
| 18.1 | 349 | Dựng bắt tay TLS 1.3 hậu lượng tử hoàn toàn bằng OpenSSL: nhóm khóa lai cộng chứng thư ML-DSA. | KHÔNG CHẠY | 0.0 s | [ma_nguon_18_01_dung_bat_tay_tls_1.sh](../ch18/ma_nguon_18_01_dung_bat_tay_tls_1.sh) |
| 19.1 | 359 | Phần lõi của công cụ kiểm kê chứng thư: đọc một chứng thư và tính điểm ưu tiên thay thế. Bị Shor phá, độ mạnh thấp và tuổi thọ còn dài đều nâng mức cấp bách. | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_19_01.txt](ch19/ma_nguon_19_01.txt) |
| 19.1b | 359 | (khối mã không đánh số, sau Mã nguồn 19.1) | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_19_01b.txt](ch19/ma_nguon_19_01b.txt) |
| 19.1c | 359 | (khối mã không đánh số, sau Mã nguồn 19.1) | CHẠY ĐƯỢC | 1.2 s | [ma_nguon_19_01c.txt](ch19/ma_nguon_19_01c.txt) |
| 20.1a | 372 | (khối mã không đánh số, đứng trước Mã nguồn 20.1) | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_20_01a.txt](ch20/ma_nguon_20_01a.txt) |
| 20.1 | 372 | BFV thu nhỏ: sinh khóa, mã hóa và giải mã. So sánh với K-PKE ở Chương 7 sẽ thấy cấu trúc gần như trùng khớp. | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_20_01.txt](ch20/ma_nguon_20_01.txt) |
| 20.1b | 372 | (khối mã không đánh số, sau Mã nguồn 20.1) | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_20_01b.txt](ch20/ma_nguon_20_01b.txt) |
| 20.1c | 372 | (khối mã không đánh số, sau Mã nguồn 20.1) | CHẠY ĐƯỢC | 0.0 s | [ma_nguon_20_01c.txt](ch20/ma_nguon_20_01c.txt) |

## Chi tiết các mã nguồn có vấn đề

### Mã nguồn 4.1 (LỆCH SÁCH)
- dòng 1: sách `== ML-KEM (FIPS 203) ==` / thực tế `OK  ML-KEM-512   (800, 1632, 768) vs (800, 1632, 768)`
- dòng 2: sách `  OK  ML-KEM-512    tinh=(800, 1632, 768)      cong_bo=(800, 1632, 768)` / thực tế `OK  ML-KEM-768   (1184, 2400, 1088) vs (1184, 2400, 1088)`
- dòng 3: sách `  OK  ML-KEM-768    tinh=(1184, 2400, 1088)    cong_bo=(1184, 2400, 1088)` / thực tế `OK  ML-KEM-1024  (1568, 3168, 1568) vs (1568, 3168, 1568)`
- dòng 4: sách `  OK  ML-KEM-1024   tinh=(1568, 3168, 1568)    cong_bo=(1568, 3168, 1568)` / thực tế `<không có>`
- dòng 5: sách `== HQC (dac ta 2025-08-22) ==` / thực tế `<không có>`
- dòng 6: sách `  OK  HQC-1         tinh=(2241, 2321, 4433)    cong_bo=(2241, 2321, 4433)` / thực tế `<không có>`
- dòng 7: sách `  OK  HQC-3         tinh=(4514, 4602, 8978)    cong_bo=(4514, 4602, 8978)` / thực tế `<không có>`
- dòng 8: sách `  OK  HQC-5         tinh=(7237, 7333, 14421)   cong_bo=(7237, 7333, 14421)` / thực tế `<không có>`
- dòng 9: sách `== Classic McEliece ==` / thực tế `<không có>`
- dòng 10: sách `  mceliece348864    |pk| =   261 120 B (  255,0 KiB)   |ct| =  96 B` / thực tế `<không có>`
- dòng 11: sách `  mceliece6960119   |pk| = 1 047 319 B (1 022,8 KiB)   |ct| = 194 B` / thực tế `<không có>`
- dòng 12: sách `  mceliece8192128   |pk| = 1 357 824 B (1 326,0 KiB)   |ct| = 208 B` / thực tế `<không có>`

### Mã nguồn 7.2c (TRÍCH ĐOẠN)
```
Traceback (most recent call last):
  File "ch07/ma_nguon_7_02c_hai_ham_cua_lop_ngoai_tiep.py", line 5, in <module>
    d = json.load(open("ML-KEM-keyGen-FIPS203.internalProjection.json"))
        ^^^^
NameError: name 'json' is not defined
```

