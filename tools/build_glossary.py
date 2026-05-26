#!/usr/bin/env python3
"""Scan source .adoc files for Bitcoin terms and build a glossary scaffold."""

import re
import json
from pathlib import Path

SOURCE_DIR = Path("bitcoinbook-third_edition_print1")
OUTPUT_FILE = Path("swahili/glossary_scaffold.adoc")
SEED_FILE = Path("tools/glossary_seed.json")


def extract_index_terms(text: str) -> set:
    """Extract terms from AsciiDoc index markers: ((("term")))."""
    pattern = r'\(\(\("([^"]+)"'
    return {m.group(1).lower() for m in re.finditer(pattern, text)}


def load_seed_terms(seed_file: Path) -> list:
    with open(seed_file, encoding="utf-8") as f:
        return json.load(f)


def scan_source_files(source_dir: Path) -> set:
    terms = set()
    for pattern in ("*.adoc", "*.asciidoc"):
        for adoc_file in source_dir.glob(pattern):
            text = adoc_file.read_text(encoding="utf-8")
            terms.update(extract_index_terms(text))
    return terms


def build_scaffold(scanned_terms: set, seed_terms: list) -> str:
    seed_by_english = {t["english"].lower(): t for t in seed_terms}
    all_terms = dict(seed_by_english)

    for term in scanned_terms:
        if term not in all_terms:
            all_terms[term] = {"english": term, "swahili": "", "type": ""}

    lines = [
        "// TRANSLATION METADATA",
        "// source: glossary.asciidoc",
        "// translator:",
        "// date:",
        "// status: draft",
        "// glossary-version: 1.0",
        "",
        "= Faharasa / Glossary",
        "",
    ]

    for english, data in sorted(all_terms.items()):
        swahili = data.get("swahili", "").strip()
        term_type = data.get("type", "").strip()
        display = swahili if swahili else "[TAFSIRI INAHITAJIKA]"
        anchor = english.replace(" ", "-").replace("/", "-")
        lines.append(f"[[term-{anchor}]]")
        lines.append(f"{english}::")
        lines.append(f"  [type:{term_type}] {display}")
        lines.append("")

    return "\n".join(lines)


def main():
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    seed_terms = load_seed_terms(SEED_FILE)
    scanned_terms = scan_source_files(SOURCE_DIR)
    scaffold = build_scaffold(scanned_terms, seed_terms)
    OUTPUT_FILE.write_text(scaffold, encoding="utf-8")
    print(f"Scaffold written to {OUTPUT_FILE}")
    print(f"Scanned terms: {len(scanned_terms)}, Seed terms: {len(seed_terms)}")


if __name__ == "__main__":
    main()
