#!/usr/bin/env python3
"""Validate AsciiDoc structure and metadata of a translated file."""

import re
import sys
from pathlib import Path

REQUIRED_HEADER_FIELDS = [
    "// source:",
    "// translator:",
    "// date:",
    "// status:",
    "// glossary-version:",
]

BLOCK_DELIMITERS = ("====", "----", "****", "____", "....", "++++")


def _strip_code_blocks(text: str) -> str:
    """Remove content between ---- delimiters so code listings are not scanned."""
    return re.sub(r"(?ms)^----$.*?^----$", "", text)


def check_metadata_header(text: str) -> list:
    """Return issues for any missing required metadata header fields."""
    header = "\n".join(text.splitlines()[:20])
    return [
        f"  Missing header field: {field}"
        for field in REQUIRED_HEADER_FIELDS
        if field not in header
    ]


def check_anchors(text: str) -> list:
    """Return issues for cross-references that have no matching anchor definition."""
    prose = _strip_code_blocks(text)
    anchors = set(re.findall(r"\[\[([^\]\n]+)\]\]", prose))
    xrefs = set(re.findall(r"<<([^,>\s]+)[,>]", prose))
    return [
        f"  Broken cross-reference: <<{xref}>>"
        for xref in xrefs
        if xref not in anchors
    ]


def check_blocks(text: str) -> list:
    issues = []
    for delim in BLOCK_DELIMITERS:
        count = sum(1 for line in text.splitlines() if line.strip() == delim)
        if count % 2 != 0:
            issues.append(f"  Unclosed block delimiter: {delim} (appears {count} times)")
    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_adoc.py <path/to/translated.adoc>")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)

    text = filepath.read_text(encoding="utf-8")
    all_issues = (
        check_metadata_header(text)
        + check_anchors(text)
        + check_blocks(text)
    )

    if not all_issues:
        print(f"OK: {filepath.name} passes all structural checks.")
        return

    print(f"ISSUES in {filepath.name}:")
    for issue in all_issues:
        print(issue)
    sys.exit(1)


if __name__ == "__main__":
    main()
