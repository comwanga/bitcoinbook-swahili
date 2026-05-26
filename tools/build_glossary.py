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
    pattern = r'\(\(\("([^"]+)"[^)]*\)\)\)'
    return {m.group(1).lower() for m in re.finditer(pattern, text)}


def load_seed_terms(seed_file: Path) -> list:
    if not seed_file.exists():
        raise FileNotFoundError(f"Seed file not found: {seed_file}. Expected at {seed_file.resolve()}")
    try:
        with open(seed_file, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in seed file {seed_file}: {e}") from e


def scan_source_files(source_dir: Path) -> set:
    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {source_dir.resolve()}")
    terms = set()
    for pattern in ("*.adoc", "*.asciidoc"):
        for adoc_file in source_dir.glob(pattern):
            try:
                text = adoc_file.read_text(encoding="utf-8")
                terms.update(extract_index_terms(text))
            except OSError as e:
                print(f"Warning: could not read {adoc_file}: {e}")
    return terms


def build_scaffold(scanned_terms: set, seed_terms: list) -> str:
    # Key by lowercase for dedup; store original casing from seed
    seed_by_lower = {t["english"].lower(): t for t in seed_terms}
    all_terms = dict(seed_by_lower)  # keyed by lowercase

    for term in scanned_terms:  # already lowercase from extract_index_terms
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

    for _key, data in sorted(all_terms.items()):
        english = data.get("english", _key)
        swahili = data.get("swahili", "").strip()
        term_type = data.get("type", "").strip()
        display = swahili if swahili else "[TAFSIRI INAHITAJIKA]"
        anchor = re.sub(r"[^a-zA-Z0-9\-]", "-", english.replace(" ", "-"))
        anchor = re.sub(r"-+", "-", anchor).strip("-").lower()
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
