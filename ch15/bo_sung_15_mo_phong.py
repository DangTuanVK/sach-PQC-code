# Không có trong sách: biên dịch và mô phỏng khối cánh bướm (Mã nguồn 15.1) với testbench bo_sung_15_tb.sv. Tái tạo kết quả in sau Mã nguồn 15.1 (chapters/ch16/main.tex).
# Testbench nap nguyen van Ma nguon 16.1 (module butterfly) va 16.1b (ham mont_ref).
# Dung Synopsys VCS neu co tren PATH, neu khong thu Siemens Questa (vlog/vsim).
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DAY = Path(__file__).resolve().parent
RTL = next(DAY.glob("ma_nguon_15_01_*.sv"))
REF = next(DAY.glob("ma_nguon_15_01b_*.sv"))
TB = DAY / "bo_sung_15_tb.sv"

def chay(lenh, cwd):
    p = subprocess.run(lenh, cwd=cwd, capture_output=True, text=True, timeout=600)
    if p.returncode != 0:
        sys.exit("loi khi chay %s:\n%s" % (lenh[0], (p.stdout + p.stderr)[-2000:]))
    return p.stdout

def co_vcs():
    """Co Synopsys VCS tren PATH (tranh nham voi lenh 'vcs' khac, vd. vcstool)."""
    if not shutil.which("vcs"):
        return False
    p = subprocess.run(["vcs", "-ID"], capture_output=True, text=True)
    return "vcs script version" in p.stdout + p.stderr

with tempfile.TemporaryDirectory() as tmp:
    tb = Path(tmp) / "tb.sv"
    tb.write_text(TB.read_text().replace("MONT_REF_FILE", str(REF)))
    if co_vcs():
        chay(["vcs", "-sverilog", "-full64", "-q", str(tb), str(RTL)], tmp)
        ra = chay(["./simv"], tmp)
    elif shutil.which("vlog") and shutil.which("vsim"):
        chay(["vlog", "-sv", "-quiet", str(tb), str(RTL)], tmp)
        ra = chay(["vsim", "-c", "-quiet", "tb", "-do", "run -all; quit -f"], tmp)
    else:
        sys.exit("khong tim thay trinh mo phong SystemVerilog (vcs hoac vlog/vsim)")

for dong in ra.splitlines():
    if re.search(r"KET QUA|BUTTERFLY|LECH|finish at", dong):
        print(re.sub(r"^#\s*", "", dong.strip()))   # Questa them "# " dau dong
