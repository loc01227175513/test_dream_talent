#!/usr/bin/env python3
"""Turn BMAD docs (out/brief.md + out/SRS.md) into a Karpathy-pattern wiki (index.md + [[wikilinks]])
that Understand-Anything's /understand-knowledge turns into a knowledge graph.

Usage: python3 wiki.py [dest=wiki]
"""
import re, sys
from collections import defaultdict
from pathlib import Path

ACTORS = {
    "A1": ("Người mua/thuê", "F-01 F-02 F-03 F-04 F-06 F-07 F-08 F-09 F-25 F-26 F-27 F-28 F-29 F-31 F-34 F-36 F-37 F-39 F-40"),
    "A2": ("Chủ nhà (FSBO)", "F-10 F-11 F-12 F-13 F-14 F-15 F-16 F-17"),
    "A3": ("Môi giới", "F-10 F-11 F-14 F-16 F-19 F-20 F-21 F-22 F-24"),
    "A4": ("Doanh nghiệp / Sàn BĐS", "F-21"),
    "A5": ("Cộng tác viên", "F-23"),
    "A6": ("AI Agent bên thứ ba", "F-45 F-46 F-47 F-48"),
    "A7": ("Admin / Chuyên viên MOSO", "F-09 F-15 F-19 F-43"),
}
INTEGRATIONS = {
    "I-Bank": ("13+ ngân hàng đối tác", "F-08 F-25 F-27"),
    "I-IEM": ("IEM — Viện Kinh tế & Quản lý", "F-22"),
    "I-Voucher": ("Urbox / Gotit e-voucher", "F-23"),
    "I-AI": ("LLM / Vision AI", "F-03 F-10 F-13 F-36 F-40"),
    "I-Maps": ("Bản đồ số", "F-04"),
    "I-OTP": ("SMS OTP (giả định)", "F-19 F-41"),
    "I-Pay": ("Cổng thanh toán (giả định)", "F-17"),
    "I-Store": ("App Store / Google Play", "F-44"),
}


def parse(brief, srs):
    """-> modules {M: name}, features {F: (name, desc, module)}, reqs {FR: (title, [F])}"""
    modules, features, cur = {}, {}, None
    for line in brief.splitlines():
        if m := re.match(r"### (M\d+) · (.*)", line):
            cur = m.group(1); modules[cur] = m.group(2).strip()
        elif cur and (m := re.match(r"\| (F-\d+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|", line)):
            features[m.group(1)] = (m.group(2).strip(), f"{m.group(3).strip()} (nguồn: {m.group(4).strip()})", cur)
    reqs = {}
    for blk in re.split(r"\n(?=#### FR-)", srs):
        if m := re.match(r"#### (FR-\d+) (.*)", blk):
            t = re.search(r"Truy vết:\*\* ([^\n]+)", blk)
            reqs[m.group(1)] = (m.group(2).strip(), re.findall(r"F-\d+", t.group(1) if t else ""))
    for m in re.finditer(r"^\| (FR-\d+) \| ([^|]+) \|.*\| (F-[\d, F-]+) \|$", srs, re.M):
        reqs[m.group(1)] = (m.group(2).strip(), re.findall(r"F-\d+", m.group(3)))
    return modules, features, reqs


def build_wiki(brief, srs, dest):
    dest = Path(dest); dest.mkdir(parents=True, exist_ok=True)
    modules, features, reqs = parse(brief, srs)
    links = defaultdict(set)  # page -> linked pages (both directions, so the graph is navigable)
    def link(a, b): links[a].add(b); links[b].add(a)
    for f, (_, _, m) in features.items(): link(m, f)
    for r, (_, fs) in reqs.items():
        for f in fs:
            if f in features: link(f, r)
    for group in (ACTORS, INTEGRATIONS):
        for k, (_, fs) in group.items():
            for f in fs.split(): link(k, f)
    pages = {m: ("Module", n, "") for m, n in modules.items()}
    pages |= {f: ("Feature", n, d) for f, (n, d, _) in features.items()}
    pages |= {r: ("Requirement", t, "") for r, (t, _) in reqs.items()}
    pages |= {k: ("Actor", n, "") for k, (n, _) in ACTORS.items()}
    pages |= {k: ("Integration", n, "") for k, (n, _) in INTEGRATIONS.items()}
    written = []
    for pid, (cat, name, desc) in pages.items():
        rel = "\n".join(f"- [[{x}]] {pages[x][1]}" for x in sorted(links[pid]) if x in pages)
        p = dest / f"{pid}.md"
        p.write_text(f"# {pid} — {name}\n\ncategory: {cat}\n\n{desc}\n\n## Liên quan\n{rel}\n")
        written.append(p)
    idx = ["# MOSO.vn — Knowledge Wiki", "", "Sinh từ tài liệu BMAD (brief.md, SRS.md)."]
    for cat in ("Actor", "Module", "Feature", "Requirement", "Integration"):
        idx += ["", f"## {cat}s"] + [f"- [[{k}]] {v[1]}" for k, v in pages.items() if v[0] == cat]
    (dest / "index.md").write_text("\n".join(idx) + "\n")
    return written + [dest / "index.md"]


def broken_links(dest):
    dest = Path(dest)
    return [f"{p.name} -> {t}" for p in sorted(dest.glob("*.md"))
            for t in re.findall(r"\[\[([^\]]+)\]\]", p.read_text()) if not (dest / f"{t}.md").exists()]


if __name__ == "__main__":
    dest = Path(sys.argv[1] if len(sys.argv) > 1 else "wiki")
    files = build_wiki(Path("out/brief.md").read_text(), Path("out/SRS.md").read_text(), dest)
    bad = broken_links(dest)
    print(f"{len(files)} pages -> {dest}/", *bad, sep="\n")
    sys.exit(1 if bad else 0)
