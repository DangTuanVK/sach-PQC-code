# Mã nguồn của sách "Mật mã hậu lượng tử"

Mã nguồn đi kèm sách **Mật mã hậu lượng tử -- Từ nền tảng toán học đến chuẩn
NIST, triển khai phần cứng và lộ trình chuyển đổi lượng tử** (TS. Đặng Minh
Tuấn). Kho gồm hai loại tệp:

- **46 khối mã in trong sách** (40 Python, 3 C, 2 SystemVerilog, 1 bash), mỗi
  tệp đánh số đúng như "Mã nguồn X.Y" trong sách và giống hệt nội dung in;
- **chương trình chạy thử bổ sung** (`bo_sung_*.py`), không in trong sách, nạp
  đúng mã của sách, bổ sung phần sách lược bỏ và in ra đúng các dòng "kết quả
  chạy" trong sách.

## Cấu trúc

```
chXX/ma_nguon_X_YY_<ten>.<py|c|sv|sh>   mã nguồn X.Y của Chương X, giống hệt trong sách
chXX/bo_sung_X_<ten>.py                 chương trình bổ sung, không in trong sách
du_lieu/acvp/                           vector kiểm thử ACVP của NIST (ML-KEM, ML-DSA)
ket_qua/chXX/*.txt                      kết quả khi chạy (stdout, stderr)
ket_qua/BAO_CAO.md                      bảng tổng hợp: trang, nội dung, trạng thái
extract.py                              trích mã từ mã LaTeX của sách
bo_sung.json                            chương trình bổ sung nào tái tạo khối kết quả nào
resolve_deps.py                         tìm phụ thuộc giữa các mã nguồn (deps.json)
run_all.py                              chạy tất cả, lưu kết quả, so với sách
```

Số mã nguồn trong sách đánh chung cho mọi ngôn ngữ. Khối mã không có số riêng
vì là phần nối tiếp của mã nguồn ngay trước mang hậu tố `b`, `c`, ví dụ
`ma_nguon_10_01b_...py`; khối không đánh số đứng trước mã nguồn đầu tiên của
chương mang hậu tố `a`, ví dụ `ma_nguon_20_01a_...py`.

## Chương trình bổ sung

Sách chỉ in phần cốt lõi của nhiều cài đặt; phần gọi thử và các hàm phụ trợ
được lược bỏ. Các tệp `bo_sung_*.py` dựng lại phần đó:

| Tệp | Tái tạo kết quả in sau |
|---|---|
| `ch03/bo_sung_3_thi_nghiem.py` | Mã nguồn 3.2: bốn thí nghiệm tấn công CCA và bọc FO |
| `ch06/bo_sung_6_doi_chieu.py` | Mã nguồn 6.3: đối chiếu NTT với phép nhân trực tiếp |
| `ch07/bo_sung_7_mlkem.py` | (module) ML-KEM đầy đủ theo FIPS 203, dùng `encaps`/`decaps`, `sample_ntt` của sách |
| `ch07/bo_sung_7_acvp.py` | Mã nguồn 7.2: đối chiếu vector ACVP keyGen, encaps, decaps |
| `ch07/bo_sung_7_tu_choi.py` | Đếm ứng viên bị loại của SampleNTT |
| `ch08/bo_sung_8_mldsa.py` | (module) ML-DSA đầy đủ theo FIPS 204, dùng `sign_internal` của sách |
| `ch08/bo_sung_8_acvp.py` | Mã nguồn 8.1: đối chiếu vector ACVP keyGen, sigGen |
| `ch10/bo_sung_10_wots_merkle.py` | Mã nguồn 10.1: WOTS+ và cây Merkle h = 4 |
| `ch11/bo_sung_11_fors.py` | Mã nguồn 11.2: FORS với n = 16, a = 4, k = 8 |
| `ch12/bo_sung_12_mceliece.py` | (module) Goppa, sinh khóa và mã hóa McEliece thu nhỏ |
| `ch12/bo_sung_12_vong_doi.py` | Mã nguồn 12.1: vòng đời McEliece với ba bộ tham số |
| `ch14/bo_sung_14_uov.py` | (module) F_16, sinh khóa và xác minh UOV thu nhỏ |
| `ch14/bo_sung_14_ky.py` | Mã nguồn 14.1: ký UOV với bốn cấu hình |
| `ch18/bo_sung_18_tls.py` | Mã nguồn 18.1: chạy tự động các lệnh OpenSSL |

Khi một hàm của sách gọi hàm phụ trợ không in trong sách, tệp bổ sung định
nghĩa hàm đó và gán vào module của sách; tệp `ma_nguon_*` không bị sửa. Các
chương trình có dùng số ngẫu nhiên đặt hạt giống cố định 2026.

## Phụ thuộc giữa các mã nguồn

Một số mã nguồn dùng lại định nghĩa của khối trước, ví dụ phép nhân bản mã BFV
(Mã nguồn 20.1b) dùng hàm `modpm` của khối 20.1a. Để mỗi tệp chạy độc lập
được, đầu tệp có thêm một khối được đánh dấu rõ:

```python
# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ Mã nguồn 20.1a ---
import contextlib as _ctx, io as _io
with _ctx.redirect_stdout(_io.StringIO()):
    from ma_nguon_20_01a_doan_ma_mo_dau import *  # noqa
# --- Hết phần thêm ---
```

Khối này nhập định nghĩa từ mã nguồn trước và tắt phần in ra của nó. Phần còn
lại của tệp giống hệt sách. Danh sách phụ thuộc nằm trong `deps.json`.

## Cài đặt và chạy

Mã in trong sách chạy được với Python 3.6 trở lên; kho được kiểm thử với Python
3.11. Hầu hết tệp chỉ cần thư viện chuẩn; Mã nguồn 7.1 cần `numpy`, Mã nguồn
1.1 cần `cryptography`, `bo_sung_18_tls.py` cần OpenSSL 3.5 trở lên.

```bash
# Cách 1: conda / micromamba
micromamba env create -f environment.yml
micromamba run -n pqcbook python run_all.py

# Cách 2: pip
pip install -r requirements.txt
python run_all.py
```

Chạy một tệp riêng lẻ (đứng trong thư mục chương để các dòng import tìm thấy
mã nguồn phụ thuộc):

```bash
cd ch08
python bo_sung_8_acvp.py
```

Chạy vài tệp qua `run_all.py`: `python run_all.py 2_02 bo_sung_8_acvp`.

Mã nguồn 19.1c là công cụ dòng lệnh kiểm kê chứng thư; `run_all.py` gọi nó với
kho chứng thư gốc của hệ thống `/etc/pki/tls/certs/ca-bundle.crt` (Linux họ Red
Hat). Trên hệ thống khác, truyền đường dẫn tới một tệp PEM bất kỳ.

Mã C (Chương 6, 15) và SystemVerilog (Chương 16) không được chạy tự động: mã C
là các hàm rời cần ghép vào chương trình riêng, mã SystemVerilog cần trình mô
phỏng như Icarus Verilog, VCS hoặc Questa.

## Kết quả kiểm tra

Với Python 3.11, numpy 2.4, cryptography 50 và OpenSSL 3.6, toàn bộ 50 tệp
Python (40 khối của sách và 10 chương trình bổ sung) chạy không lỗi. 14 trong 16
khối "kết quả chạy" in trong sách được tái tạo và trùng từng dòng; chi tiết
trong [ket_qua/BAO_CAO.md](ket_qua/BAO_CAO.md). Hai khối còn lại không so tự
động: kết quả mô phỏng SystemVerilog ở Chương 16 (testbench không in trong sách)
và danh sách nhóm của `openssl list -tls-groups` ở Chương 18 (sách in dạng rút
gọn).

Khi so với sách, `run_all.py` bỏ qua những phần phụ thuộc máy chạy: cột thời
gian đo (Chương 6, 12, 14) và ngày chạy (Mã nguồn 19.1c). Các biểu thức bỏ qua
khai báo trong `bo_sung.json`.

## Cập nhật khi sách thay đổi

```bash
python extract.py ../sach-PQC     # trích lại từ mã LaTeX của sách
python resolve_deps.py            # (khi có mã nguồn mới) tìm lại phụ thuộc
python run_all.py                 # chạy lại và cập nhật ket_qua/
```

## Giấy phép

Mã nguồn phát hành theo giấy phép MIT, xem [LICENSE](LICENSE). Vector kiểm thử
trong `du_lieu/acvp/` lấy từ kho
[usnistgov/ACVP-Server](https://github.com/usnistgov/ACVP-Server) của NIST.
