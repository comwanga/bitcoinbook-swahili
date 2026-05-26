#!/usr/bin/env python3
"""Show translation progress for all source files."""

import re
from pathlib import Path

SWAHILI_DIR = Path(__file__).parent.parent / "swahili"

TRANSLATION_ORDER = [
    "glossary.asciidoc",
    "preface.adoc",
    "ch01_intro.adoc",
    "ch02_overview.adoc",
    "ch03_bitcoin-core.adoc",
    "ch04_keys.adoc",
    "ch05_wallets.adoc",
    "ch06_transactions.adoc",
    "ch07_authorization-authentication.adoc",
    "ch08_signatures.adoc",
    "ch09_fees.adoc",
    "ch10_network.adoc",
    "ch11_blockchain.adoc",
    "ch12_mining.adoc",
    "ch13_security.adoc",
    "ch14_applications.adoc",
    "appa_whitepaper.adoc",
    "appb_errata.adoc",
    "appc_bips.adoc",
    "tapscript.asciidoc",
]

STATUS_ICONS = {
    "missing":  "[ ]",
    "draft":    "[~]",
    "reviewed": "[*]",
    "final":    "[x]",
}


def get_status(filepath: Path) -> str:
    if not filepath.exists():
        return "missing"
    text = filepath.read_text(encoding="utf-8")
    header = "\n".join(text.splitlines()[:10])
    match = re.search(r"^//\s*status:\s*(\w+)", header, re.MULTILINE)
    if match:
        status = match.group(1)
        if status in STATUS_ICONS:
            return status
    return "draft"


def word_count(filepath: Path) -> int:
    if not filepath.exists():
        return 0
    text = filepath.read_text(encoding="utf-8")
    text = re.sub(r"//.*", "", text)                    # strip comments
    text = re.sub(r"\(\(\(.*?\)\)\)", "", text)         # strip index terms
    text = re.sub(r"\[\[.*?\]\]", "", text)             # strip anchors
    text = re.sub(r"^\[.*?\]$", "", text, flags=re.MULTILINE)   # strip block annotations
    text = re.sub(r"^=+\s*", "", text, flags=re.MULTILINE)      # strip heading markers
    return len(text.split())


def main():
    print(f"\n{'':4}{'File':<52} {'Status':<10} {'Words':>7}")
    print("-" * 76)
    done = 0
    for filename in TRANSLATION_ORDER:
        path = SWAHILI_DIR / filename
        status = get_status(path)
        words = word_count(path)
        icon = STATUS_ICONS.get(status, "[ ]")
        print(f"{icon}  {filename:<52} {status:<10} {words:>7}")
        if status in ("reviewed", "final"):
            done += 1
    print("-" * 76)
    print(f"Progress: {done}/{len(TRANSLATION_ORDER)} files reviewed or final\n")


if __name__ == "__main__":
    main()
