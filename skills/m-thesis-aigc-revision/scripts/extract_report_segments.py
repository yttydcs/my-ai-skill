#!/usr/bin/env python3
import argparse
import html
import re
import sys
from pathlib import Path


ROW_PATTERN = re.compile(
    r'<div class="fake_table_tr clear">\s*'
    r'<div class="single_table_item w72">(?P<idx>\d+)</div>\s*'
    r'<div class="single_table_item w444">.*?'
    r'<span class="hide_3">(?P<text>.*?)</span>.*?'
    r'<div class="single_table_item w159">(?P<words>\d+)</div>\s*'
    r'<div class="single_table_item w160">(?P<ratio>[\d.]+%)</div>',
    re.S,
)


def clean_text(raw: str) -> str:
    text = re.sub(r"<.*?>", " ", raw)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract suspicious segment summaries from an AIGC report HTML."
    )
    parser.add_argument("report", help="Path to the report HTML file")
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Maximum number of rows to print (default: 10)",
    )
    parser.add_argument(
        "--preview-chars",
        type=int,
        default=90,
        help="Preview length per row (default: 90)",
    )
    args = parser.parse_args()

    report_path = Path(args.report)
    if not report_path.exists():
        print(f"Report not found: {report_path}", file=sys.stderr)
        return 1

    content = report_path.read_text(encoding="utf-8", errors="ignore")
    matches = list(ROW_PATTERN.finditer(content))
    if not matches:
        print("No suspicious-segment table rows found.", file=sys.stderr)
        return 2

    for match in matches[: args.top]:
        text = clean_text(match.group("text"))
        preview = text[: args.preview_chars]
        print(
            f"[{match.group('idx')}] ratio={match.group('ratio')} "
            f"words={match.group('words')} preview={preview}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
