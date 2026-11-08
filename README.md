# Mã nguồn của sách "Mật mã hậu lượng tử"

Mã nguồn đi kèm sách **Mật mã hậu lượng tử -- Từ nền tảng toán học đến chuẩn
NIST, triển khai phần cứng và lộ trình chuyển đổi lượng tử** (TS. Đặng Minh
Tuấn). Thư mục này chứa toàn bộ 46 khối mã in trong 20 chương của sách: 40 khối
Python, 3 khối C, 2 khối SystemVerilog và 1 khối bash. Mỗi file được đánh số
đúng như "Mã nguồn X.Y" trong sách; các khối Python đã được chạy thử và kết quả
lưu trong `ket_qua/`.

## Cấu trúc

```
chXX/ma_nguon_X_YY_<ten>.<py|c|sv|sh>   mã nguồn X.Y của Chương X, giống hệt trong sách
ket_qua/chXX/ma_nguon_X_YY.txt          kết quả khi chạy (stdout, stderr)
ket_qua/chXX/ma_nguon_X_YY_tep/         file do mã nguồn tạo ra (ví dụ cbom.json)
ket_qua/BAO_CAO.md                      bảng tổng hợp: trang, nội dung, trạng thái
extract.py                              trích mã từ mã LaTeX của sách
resolve_deps.py                         tìm phụ thuộc giữa các mã nguồn (deps.json)
run_all.py                              chạy tất cả, lưu kết quả, so với sách
```

Số mã nguồn trong sách đánh chung cho mọi ngôn ngữ. Một số khối mã trong sách
không có số riêng vì là phần nối tiếp của mã nguồn ngay trước; các file này mang
hậu tố `b`, `c`, ví dụ `ma_nguon_10_01b_...py`. Khối không đánh số đứng trước mã
nguồn đầu tiên của chương mang hậu tố `a`, ví dụ `ma_nguon_20_01a_...py`.

## Phụ thuộc giữa các mã nguồn

Một số mã nguồn dùng lại định nghĩa của khối trước, ví dụ phép nhân bản mã BFV
(Mã nguồn 20.1b) dùng hàm `modpm` của khối 20.1a. Để mỗi file chạy độc lập
được, đầu file có thêm một khối được đánh dấu rõ:

```python
# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 20.1a ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_20_01a_doan_ma_mo_dau import *  # noqa
# --- Hết phần thêm ---
```

Khối này nhập định nghĩa từ mã nguồn trước và tắt phần in ra của nó. Phần còn
lại của file giống hệt sách. Danh sách phụ thuộc nằm trong `deps.json`.

## Cài đặt và chạy

Mã Python cần Python 3.10 trở lên, `numpy` (Chương 7) và `cryptography` (đọc
chứng thư X.509 ở Chương 1 và Chương 19).

```bash
# Cách 1: conda / micromamba
micromamba env create -f environment.yml
micromamba run -n pqcbook python run_all.py

# Cách 2: pip
pip install -r requirements.txt
python run_all.py
```

Chạy một mã nguồn riêng lẻ (cần đứng trong thư mục chương để các dòng import
tìm thấy mã nguồn phụ thuộc):

```bash
cd ch06
python ma_nguon_6_01_ntt_va_intt_chung_cho.py
```

Chạy vài mã nguồn qua `run_all.py`: `python run_all.py 2_02 11_01`.

Mã nguồn 19.1c là công cụ dòng lệnh kiểm kê chứng thư; `run_all.py` gọi nó với
kho chứng thư gốc của hệ thống `/etc/pki/tls/certs/ca-bundle.crt` (Linux họ Red
Hat). Trên hệ thống khác, truyền đường dẫn tới một tệp PEM bất kỳ.

Mã C (Chương 6, 15), SystemVerilog (Chương 16) và bash (Chương 18) không được
chạy tự động. Mã C là các hàm rời, cần ghép vào chương trình riêng; mã
SystemVerilog cần trình mô phỏng như Icarus Verilog, VCS hoặc Questa; lệnh bash
cần OpenSSL 3.5 trở lên.

## Kết quả kiểm tra

Với Python 3.11, numpy 2.4 và cryptography 50, 39 trong 40 khối Python chạy
không lỗi. Chi tiết từng khối trong [ket_qua/BAO_CAO.md](ket_qua/BAO_CAO.md).

- **Khớp sách**: Mã nguồn 2.2 và 11.1 in đúng từng dòng như "Kết quả chạy"
  trong sách.
- **Chỉ định nghĩa**: sáu khối (3.2b, 6.3, 10.1b, 11.2, 12.1b, 14.1) chỉ định
  nghĩa hàm. Chúng chạy không lỗi nhưng không in gì, vì kết quả in trong sách
  đến từ phần gọi thử không in trong sách.
- **Trích đoạn**: Mã nguồn 7.2c nạp bộ vector kiểm thử ACVP của NIST và gọi các
  hàm của một cài đặt ML-KEM đầy đủ không in trong sách, nên không chạy độc lập.
- **Lệch sách**: Mã nguồn 4.1 trong sách chỉ tính kích thước cho ML-KEM; kết quả
  in ngay sau nó là của bản mở rộng cho cả HQC và Classic McEliece (sách có ghi
  rõ), với định dạng dòng in khác.

Một số mã nguồn dùng số ngẫu nhiên không cố định hạt giống, đo thời gian chạy,
hoặc phụ thuộc ngày chạy (Mã nguồn 19.1c), nên kết quả của bạn có thể khác các
file trong `ket_qua/` ở những dòng đó.

## Cập nhật khi sách thay đổi

```bash
python extract.py ../sach-PQC     # trích lại từ mã LaTeX của sách
python resolve_deps.py            # (khi có mã nguồn mới) tìm lại phụ thuộc
python run_all.py                 # chạy lại và cập nhật ket_qua/
```

## Giấy phép

Mã nguồn phát hành theo giấy phép MIT, xem [LICENSE](LICENSE).
