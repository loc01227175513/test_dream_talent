#!/usr/bin/env python3
"""Gate between BMAD stages: SRS must have the required sections and only trace to features the brief defines.

Usage: python3 validate.py  (checks out/SRS.md against out/brief.md, exit 1 on errors)
"""
import re, sys
from pathlib import Path

SECTIONS = {  # name -> accepted heading words (vi | en)
    "Introduction": r"Giới thiệu|Introduction",
    "Functional Requirements": r"Yêu cầu chức năng|Functional Requirements",
    "Non-Functional Requirements": r"Yêu cầu phi chức năng|Non-Functional Requirements",
    "Epics": r"Epics?",
    "Traceability": r"Ma trận truy vết|Traceability",
}


def check_srs(srs, brief):
    headings = "\n".join(re.findall(r"^#+ .*$", srs, re.M))
    errs = [f"missing section: {n}" for n, pat in SECTIONS.items() if not re.search(pat, headings, re.I)]
    known = set(re.findall(r"F-\d+", brief))
    errs += [f"unknown feature: {f}" for f in sorted(set(re.findall(r"F-\d+", srs)) - known)]
    return errs


if __name__ == "__main__":
    errs = check_srs(Path("out/SRS.md").read_text(), Path("out/brief.md").read_text())
    print("\n".join(errs) or "SRS OK")
    sys.exit(1 if errs else 0)
