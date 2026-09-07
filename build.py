#!/usr/bin/env python3
"""Convert products.xlsx to products.json.

Reads the first sheet (or --sheet), uses row 1 as headers verbatim,
resolves =HYPERLINK("url","label") cells to the URL, preserves every
column as-is. No column is hard-coded.
"""
import argparse
import json
import re
import sys
from pathlib import Path

try:
    from openpyxl import load_workbook
except ImportError:
    sys.stderr.write(
        "openpyxl is required. Install it with:\n"
        "    pip install openpyxl\n"
    )
    sys.exit(1)


HYPERLINK_RE = re.compile(
    r'^\s*=\s*HYPERLINK\s*\(\s*"([^"]*)"\s*(?:,\s*"([^"]*)"\s*)?\)\s*$',
    re.IGNORECASE,
)


def resolve_cell(cell):
    """Return the cell's user-facing value, resolving HYPERLINK formulas."""
    if cell.hyperlink and getattr(cell.hyperlink, "target", None):
        return cell.hyperlink.target

    value = cell.value
    if isinstance(value, str):
        m = HYPERLINK_RE.match(value)
        if m:
            return m.group(1)
    if value is None:
        return ""
    return value


def convert(xlsx_path: Path, sheet_name: str | None, out_path: Path) -> int:
    wb = load_workbook(filename=str(xlsx_path), data_only=False)
    ws = wb[sheet_name] if sheet_name else wb[wb.sheetnames[0]]

    rows = ws.iter_rows()
    try:
        header_row = next(rows)
    except StopIteration:
        out_path.write_text("[]", encoding="utf-8")
        return 0

    headers = [
        (str(c.value).strip() if c.value is not None else f"col{i+1}")
        for i, c in enumerate(header_row)
    ]

    products = []
    for row in rows:
        if all(c.value is None for c in row):
            continue
        record = {}
        for i, header in enumerate(headers):
            cell = row[i] if i < len(row) else None
            if cell is None:
                record[header] = ""
                continue
            val = resolve_cell(cell)
            if hasattr(val, "isoformat"):
                val = val.isoformat()
            record[header] = val
        products.append(record)

    out_path.write_text(
        json.dumps(products, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return len(products)


def main():
    ap = argparse.ArgumentParser(description="Convert products.xlsx to products.json")
    ap.add_argument("--input", "-i", default="products.xlsx", help="Input xlsx file")
    ap.add_argument("--output", "-o", default="products.json", help="Output json file")
    ap.add_argument("--sheet", "-s", default=None, help="Sheet name (defaults to first sheet)")
    args = ap.parse_args()

    xlsx_path = Path(args.input)
    if not xlsx_path.exists():
        sys.stderr.write(f"Not found: {xlsx_path}\n")
        sys.exit(1)

    out_path = Path(args.output)
    count = convert(xlsx_path, args.sheet, out_path)
    print(f"Wrote {count} products to {out_path}")


if __name__ == "__main__":
    main()
