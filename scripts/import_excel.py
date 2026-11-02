"""One-time import of the institutions Excel into clean society records.

Usage:
    python scripts/import_excel.py              # writes data/societies.json + data/import_report.md
    python scripts/import_excel.py --overwrite  # replaces an existing (possibly hand-edited) societies.json

Review data/import_report.md, then upload with scripts/upload_json.py.
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from unisdb.text import clean, compact, normalize  # noqa: E402

DEFAULT_EXCEL = ROOT / "INSTITUCIONES DEBATE - OFICIAL 2026.xlsx"
DATA_DIR = ROOT / "data"

# Column order of the LISTA sheet.
COL_CODE, COL_INST_ACR, COL_INST, COL_COUNTRY, COL_SOC_ACR, COL_SOC, COL_VERIFIED, COL_SCHOOL, COL_OTHER = range(9)


def read_rows(excel_path: Path):
    wb = openpyxl.load_workbook(excel_path, read_only=True, data_only=True)
    ws = wb["LISTA"]
    for row_number, row in enumerate(ws.iter_rows(min_row=2, max_col=9, values_only=True), start=2):
        row = list(row) + [None] * (9 - len(row))
        if any(clean(v) for v in row[:6]):
            yield row_number, row


def split_aliases(value) -> list[str]:
    return [a for a in (clean(p) for p in re.split(r"[,;/\n]", str(value or ""))) if a]


def to_record(row_number: int, row: list) -> dict:
    institution = {"name": clean(row[COL_INST]), "acronym": clean(row[COL_INST_ACR])}
    if row[COL_SCHOOL] is True:
        kind = "escolar"
    elif institution["name"]:
        kind = "universidad"
    else:
        kind = "independiente"
    return {
        "code": clean(row[COL_CODE]),
        "country": clean(row[COL_COUNTRY]),
        "type": kind,
        "institution": institution,
        "society": {"name": clean(row[COL_SOC]), "acronym": clean(row[COL_SOC_ACR])},
        "aliases": split_aliases(row[COL_OTHER]),
        "verified": row[COL_VERIFIED] is True,
        "source_row": row_number,
    }


def find_duplicate_groups(records: list[dict]) -> list[list[dict]]:
    """Group records that share a code, a society acronym or a society name (union-find)."""
    parent = list(range(len(records)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    owner = {}
    for i, r in enumerate(records):
        keys = {("acr", compact(r["code"])), ("acr", compact(r["society"]["acronym"])),
                ("name", normalize(r["society"]["name"]))}
        for key in keys:
            if not key[1]:
                continue
            if key in owner:
                parent[find(i)] = find(owner[key])
            else:
                owner[key] = i

    groups = defaultdict(list)
    for i, r in enumerate(records):
        groups[find(i)].append(r)
    return [g for g in groups.values() if len(g) > 1]


def describe(r: dict) -> str:
    soc = r["society"]["name"] or "?"
    inst = r["institution"]["name"] or "—"
    return f"row {r['source_row']}: `{r['code'] or '(no code)'}` — {soc} ({inst}, {r['country'] or 'no country'})"


def build_report(records: list[dict]) -> tuple[str, bool]:
    """Return the markdown report and whether there are issues that block a MongoDB upload."""
    lines = ["# Import report", "", f"- Records: **{len(records)}**",
             f"- Verified: {sum(r['verified'] for r in records)}",
             f"- Types: " + ", ".join(f"{t} {sum(r['type'] == t for r in records)}"
                                     for t in ("universidad", "escolar", "independiente")), ""]

    def section(title, items, note=""):
        lines.append(f"## {title} ({len(items)})")
        if note:
            lines.append(note)
        lines.extend(f"- {item}" for item in items) if items else lines.append("- none")
        lines.append("")

    codes = defaultdict(list)
    for r in records:
        if r["code"]:
            codes[compact(r["code"])].append(r)
    dup_codes = [g for g in codes.values() if len(g) > 1]
    no_code = [r for r in records if not r["code"]]

    section("BLOCKING: duplicate codes", ["; ".join(describe(r) for r in g) for g in dup_codes],
            "Codes must be unique. Rename or merge these rows.")
    section("BLOCKING: missing code", [describe(r) for r in no_code],
            "These rows are skipped on MongoDB upload until they get a code.")
    section("Likely duplicates", ["<br>".join(describe(r) for r in g) for g in find_duplicate_groups(records)],
            "Rows sharing a code, society acronym or society name. Merge them or confirm they are different.")
    section("Missing country", [describe(r) for r in records if not r["country"]])
    section("Missing society name", [describe(r) for r in records if not r["society"]["name"]])

    by_institution = defaultdict(list)
    for r in records:
        if r["institution"]["name"]:
            by_institution[(normalize(r["institution"]["name"]), r["country"])].append(r)
    section("Institutions with several societies (info)",
            [f"{g[0]['institution']['name']}: " + ", ".join(f"`{r['code']}`" for r in g)
             for g in by_institution.values() if len(g) > 1],
            "Fine if they really are different societies; otherwise they are duplicates.")

    countries = sorted({r["country"] for r in records if r["country"]})
    section("Country spellings (check for variants)", countries)

    return "\n".join(lines), bool(dup_codes)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--excel", type=Path, default=DEFAULT_EXCEL)
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing data/societies.json")
    args = parser.parse_args()

    out = DATA_DIR / "societies.json"
    if out.exists() and not args.overwrite:
        sys.exit(f"{out} already exists and may contain manual edits. Use --overwrite to replace it.")

    records = [to_record(n, row) for n, row in read_rows(args.excel)]
    report, _ = build_report(records)

    DATA_DIR.mkdir(exist_ok=True)
    out.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATA_DIR / "import_report.md").write_text(report, encoding="utf-8")
    print(f"{len(records)} records -> {out}")
    print(f"Report -> {DATA_DIR / 'import_report.md'}")


if __name__ == "__main__":
    main()