#!/usr/bin/env python3
"""Detect inconsistent Swahili terminology across translated chapters."""

import re
import sys
from pathlib import Path

SWAHILI_DIR = Path(__file__).parent.parent / "swahili"
GLOSSARY_FILE = SWAHILI_DIR / "glossary.asciidoc"


def load_glossary(glossary_file: Path) -> dict:
    """Returns {english_term: {swahili, type}}."""
    terms = {}
    text = glossary_file.read_text(encoding="utf-8")
    pattern = r"^([\w][\w \-/]+?)::\n\s+\[type:(\w*)\]\s+(.+)$"
    for m in re.finditer(pattern, text, re.MULTILINE):
        english = m.group(1).strip()
        term_type = m.group(2).strip()
        swahili = m.group(3).strip()
        if swahili and swahili != "[TAFSIRI INAHITAJIKA]":
            terms[english] = {"swahili": swahili, "type": term_type}
    return terms


def strip_code_blocks(text: str) -> str:
    """Remove content between ---- delimiters so code listings are not scanned."""
    return re.sub(r"(?ms)^----$.*?^----$", "", text)


def check_file(filepath: Path, glossary: dict) -> list:
    issues = []
    text = filepath.read_text(encoding="utf-8")
    prose = strip_code_blocks(text)
    for english, data in glossary.items():
        if data["type"] == "preserved":
            continue
        expected_swahili = data["swahili"]
        if re.search(rf"\b{re.escape(english)}\b", prose, re.IGNORECASE):
            if not re.search(re.escape(expected_swahili), prose, re.IGNORECASE):
                issues.append(
                    f"  '{english}' found without Swahili equivalent '{expected_swahili}'"
                )
    return issues


def main():
    if not GLOSSARY_FILE.exists():
        print(f"ERROR: {GLOSSARY_FILE} not found. Run Session 1 first.")
        sys.exit(1)

    glossary = load_glossary(GLOSSARY_FILE)
    print(f"Loaded {len(glossary)} glossary terms")

    all_issues = {}
    for adoc_file in sorted(SWAHILI_DIR.glob("ch*.adoc")):
        issues = check_file(adoc_file, glossary)
        if issues:
            all_issues[adoc_file.name] = issues

    if not all_issues:
        print("No terminology inconsistencies found.")
        return

    for filename, issues in all_issues.items():
        print(f"\n{filename}:")
        for issue in issues:
            print(issue)
    sys.exit(1)


if __name__ == "__main__":
    main()
