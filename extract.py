#!/usr/bin/env python3
"""Trích các khối mã trong sách "Mật mã hậu lượng tử".

Đọc thứ tự chương từ main.tex của sách, đánh số mã nguồn đúng như LaTeX
(bộ đếm `listing` theo chương, đếm mọi ngôn ngữ), ghi mỗi khối mã ra
chXX/ma_nguon_X_YY_<ten>.<đuôi> và lập manifest.json cho run_all.py.
Khối "text" in ngay sau một khối mã được coi là kết quả chạy in trong sách.

Cách dùng:  python3 extract.py [đường_dẫn_thư_mục_sách]
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOOK = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parent / "sach-PQC"
DEPS_FILE = HERE / "deps.json"   # khai báo phụ thuộc giữa các mã nguồn
EXT = {"python": "py", "c": "c", "systemverilog": "sv", "bash": "sh"}
COMMENT = {"python": "#", "bash": "#", "c": "//", "systemverilog": "//"}
TITLE = "Mật mã hậu lượng tử (TS. Đặng Minh Tuấn)"


def slugify(caption, max_words=5):
    """Tên file ngắn từ caption: bỏ lệnh LaTeX, bỏ dấu, nối bằng '_'."""
    s = re.sub(r"\$[^$]*\$", " ", caption)            # bỏ công thức
    s = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", " ", s)  # bỏ lệnh LaTeX
    s = s.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    words = re.findall(r"[A-Za-z0-9]+", s.lower())
    return "_".join(words[:max_words]) or "ma_nguon"


def labels():
    """Số của mọi nhãn (\\label) trong sách, đọc từ các file .aux (nếu đã build)."""
    out = {}
    for aux in [BOOK / "main.aux"] + sorted(BOOK.glob("chapters/*/main.aux")):
        for m in re.finditer(r"\\newlabel\{([^}]*)\}\{\{([^}]*)\}", aux.read_text(encoding="utf-8")):
            out[m.group(1)] = m.group(2)
    return out


LABELS = {}


def plain(caption):
    """Caption LaTeX -> văn bản thường (cho chú thích code và báo cáo)."""
    s = re.sub(r"\\(?:eq)?ref\{([^}]*)\}", lambda m: LABELS.get(m.group(1), "?"), caption)
    for a, b in [(r"\\mathbb\{F\}", "F"), (r"\\mathbb\{Z\}", "Z"), (r"\\text\{([^}]*)\}", r"\1"),
                 (r"\\texttt\{([^}]*)\}", r"\1"), (r"\\emph\{([^}]*)\}", r"\1"),
                 (r"\\textbf\{([^}]*)\}", r"\1"), (r"\\mathbf\{([^}]*)\}", r"\1"),
                 (r"\\cite(\[[^\]]*\])?\{[^}]*\}", ""),
                 (r"\\gamma", "gamma"), (r"\\delta", "delta"), (r"\\neq", "!="), (r"\\le\b", "<="),
                 (r"\\times", "x"), (r"\\to", "->"), (r"\\infty", "inf"), (r"\\_", "_"),
                 (r"\$", ""), (r"[{}]", ""), (r"~", " "), (r"--", "-"), (r"\\", "")]:
        s = re.sub(a, b, s)
    return re.sub(r"\s+", " ", s).strip()


def _strip(seg):
    out = []
    for line in seg.split("\n"):
        m = re.search(r"(?<!\\)%", line)
        out.append(line[:m.start()] if m else line)
    return "\n".join(out)


def strip_comments(tex):
    """Xóa chú thích LaTeX (%) ngoài các khối minted; giữ nguyên số dòng
    và giữ nguyên nội dung code (toán tử % của Python)."""
    parts, pos = [], 0
    for m in re.finditer(r"\\begin\{minted\}.*?\\end\{minted\}", tex, re.S):
        parts.append(_strip(tex[pos:m.start()]))
        parts.append(m.group(0))
        pos = m.end()
    parts.append(_strip(tex[pos:]))
    return "".join(parts)


def chapter_files():
    main = (BOOK / "main.tex").read_text(encoding="utf-8")
    main = strip_comments(main)
    mainmatter = main[main.index("\\mainmatter"):main.index("\\appendix")]
    chapters = re.findall(r"\\include\{chapters/(ch\d+)/main\}", mainmatter)
    return [(i + 1, BOOK / "chapters" / c / "main.tex") for i, c in enumerate(chapters)]


def page_numbers():
    """Số trang của từng mã nguồn, lấy từ main.lol (nếu đã build)."""
    lol = BOOK / "main.lol"
    pages = {}
    if lol.exists():
        for m in re.finditer(r"\\numberline \{([\d.]+)\}.*?\}\}\{(\d+)\}",
                             lol.read_text(encoding="utf-8")):
            pages[m.group(1)] = int(m.group(2))
    return pages


ENV_RE = re.compile(
    r"\\begin\{listing\}|\\end\{listing\}"
    r"|\\begin\{minted\}(?:\[[^\]]*\])?\{(?P<lang>[a-z]+)\}\n(?P<code>.*?)\\end\{minted\}",
    re.S)
NEXT_MINTED = re.compile(r"\\begin\{minted\}(?:\[[^\]]*\])?\{([a-z]+)\}\n(.*?)\\end\{minted\}", re.S)


def expected_after(tex, pos):
    """Khối text in ngay sau vị trí pos (cách không quá ~700 ký tự văn bản,
    không qua tiêu đề mục) được coi là kết quả chạy in trong sách."""
    m = NEXT_MINTED.search(tex, pos)
    if not m or m.group(1) != "text":
        return None
    gap = tex[pos:m.start()]
    if len(gap) > 700 or re.search(r"\\(sub)*section|\\begin\{listing\}", gap):
        return None
    return m.group(2)


def extract_chapter(chap_no, path):
    tex = strip_comments(path.read_text(encoding="utf-8"))
    blocks, number, in_listing, suffix = [], 0, False, 0
    for m in ENV_RE.finditer(tex):
        tok = m.group(0)
        if tok.startswith("\\begin{listing}"):
            number += 1
            in_listing = True
            suffix = 0
            continue
        if tok.startswith("\\end{listing}"):
            in_listing = False
            continue
        lang = m.group("lang")
        if lang not in EXT:
            continue
        line = tex[:m.start()].count("\n") + 1
        after = tex[m.end():m.end() + 1500]
        if in_listing:
            num = f"{chap_no}.{number}"
            ident = f"{chap_no}_{number:02d}"
            cap = re.search(r"\\caption(?:\[[^\]]*\])?\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}", after)
            caption = cap.group(1) if cap else ""
            end = m.end() + after.find("\\end{listing}") + len("\\end{listing}")
        else:
            # Khối không có số: phần nối tiếp của mã nguồn ngay trước
            # (hậu tố b, c...), hoặc khối đứng trước mã nguồn đầu chương (hậu tố a)
            suffix += 1
            if number == 0:
                num, ident = f"{chap_no}.1a", f"{chap_no}_01a"
                caption = "(khối mã không đánh số, đứng trước Mã nguồn %d.1)" % chap_no
            else:
                letter = "bcdefg"[suffix - 1]
                num = f"{chap_no}.{number}{letter}"
                ident = f"{chap_no}_{number:02d}{letter}"
                caption = "(khối mã không đánh số, sau Mã nguồn %d.%d)" % (chap_no, number)
            end = m.end()
        expected = expected_after(tex, end) if lang == "python" else None
        blocks.append(dict(id=ident, number=num, chapter=chap_no, lang=lang,
                           caption=caption, tex=str(path.relative_to(BOOK)),
                           line=line, code=m.group("code"), expected=expected))
    return blocks


def header_lines(b, page, deps, by_id):
    c = COMMENT[b["lang"]]
    cap = plain(b["caption"])
    h = [f"{c} Mã nguồn {b['number']} - {cap}",
         f"{c} Sách: {TITLE}, Chương {b['chapter']}" + (f", trang {page}" if page else ""),
         f"{c} Trích tự động từ {b['tex']} (dòng {b['line']}) bằng extract.py; "
         f"không sửa tay file này."]
    if deps:
        h.append("")
        h.append("# --- Dòng thêm, không có trong sách: dùng lại định nghĩa từ "
                 + ", ".join("Mã nguồn " + by_id[d]["number"] for d in deps) + " ---")
        h.append("import contextlib as _ctx, io as _io")
        h.append("with _ctx.redirect_stdout(_io.StringIO()):")
        for d in deps:
            h.append(f"    from {Path(by_id[d]['file']).stem} import *  # noqa")
        h.append("# --- Hết phần thêm ---")
    return h


def main():
    LABELS.update(labels())
    deps_all = json.loads(DEPS_FILE.read_text(encoding="utf-8")) if DEPS_FILE.exists() else {}
    pages = page_numbers()
    blocks = []
    for chap_no, path in chapter_files():
        blocks += extract_chapter(chap_no, path)
    by_id = {}
    for b in blocks:
        base = b["number"].rstrip("abcdefg")
        if b["number"].endswith("a"):
            slug = "doan_ma_mo_dau"
        elif b["number"][-1].isalpha():
            parent = by_id[f"{b['chapter']}_{int(base.split('.')[1]):02d}"]
            slug = slugify(parent["caption"]) + "_tiep"
        else:
            slug = slugify(b["caption"])
        b["file"] = f"ch{b['chapter']:02d}/ma_nguon_{b['id']}_{slug}.{EXT[b['lang']]}"
        b["page"] = pages.get(base)
        b["deps"] = deps_all.get(b["id"], [])
        b["title"] = plain(b["caption"])
        by_id[b["id"]] = b
    # Xóa file mã nguồn cũ không còn trong sách (số mã nguồn đổi khi sách sửa)
    keep = {HERE / b["file"] for b in blocks}
    for old in HERE.glob("ch[0-9]*/ma_nguon_*"):
        if old.is_file() and old not in keep:
            old.unlink()
    for b in blocks:
        out = HERE / b["file"]
        out.parent.mkdir(parents=True, exist_ok=True)
        text = "\n".join(header_lines(b, b["page"], b["deps"], by_id)) + "\n\n" + b["code"]
        out.write_text(text, encoding="utf-8")
    manifest = [{k: v for k, v in b.items() if k != "code"} for b in blocks]
    (HERE / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    langs = {}
    for b in blocks:
        langs[b["lang"]] = langs.get(b["lang"], 0) + 1
    print(f"Đã trích {len(blocks)} khối mã từ {BOOK}: "
          + ", ".join(f"{k} {v}" for k, v in sorted(langs.items())))


if __name__ == "__main__":
    main()
