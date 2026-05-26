#!/usr/bin/env python3
"""Show translation progress for all source files."""

import re
from pathlib import Path

SWAHILI_DIR = Path("swahili")

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
    match = re.search(r"// status:\s*(\w+)", text)
    return match.group(1) if match else "draft"


def word_count(filepath: Path) -> int:
    if not filepath.exists():
        return 0
    text = filepath.read_text(encoding="utf-8")
    text = re.sub(r"//.*", "", text)
    text = re.sub(r"\[\[.*?\]\]", "", text)
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
