# Mastering Bitcoin Swahili Translation — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Python toolchain that supports consistent, validated, session-by-session Swahili translation of all 20 source `.adoc` files from *Mastering Bitcoin* 3rd Edition.

**Architecture:** A `tools/` directory contains four Python scripts — glossary builder, progress tracker, glossary validator, and AsciiDoc structure validator. The scripts operate on a `swahili/` mirror directory. Translation happens interactively session-by-session with the toolchain enforcing consistency and structure at each checkpoint.

**Tech Stack:** Python 3.10+, pytest, pathlib, re (stdlib only — no external dependencies except optional asciidoctor for final compile)

---

## File Map

| File | Role |
|---|---|
| `tools/glossary_seed.json` | Curated seed list of ~80 Bitcoin terms with suggested Swahili translations |
| `tools/build_glossary.py` | Scans source `.adoc` files + seed, outputs `swahili/glossary_scaffold.adoc` |
| `tools/translation_status.py` | Prints per-file progress table by reading metadata headers |
| `tools/validate_glossary.py` | Detects inconsistent term usage across translated chapters |
| `tools/validate_adoc.py` | Checks AsciiDoc structure: metadata header, cross-references, block delimiters |
| `tests/test_build_glossary.py` | Tests for term extraction and scaffold generation |
| `tests/test_translation_status.py` | Tests for status and word-count reading |
| `tests/test_validate_glossary.py` | Tests for glossary loading and term checking |
| `tests/test_validate_adoc.py` | Tests for anchor, block, and metadata checks |
| `swahili/glossary.asciidoc` | Master Swahili-English glossary (created in Session 1) |
| `swahili/ch01_intro.adoc` … | Translated chapter files (one per translation session) |

---

## Task 1: Project Scaffolding

**Files:**
- Create: `tools/` directory
- Create: `tests/` directory
- Create: `swahili/` directory
- Create: `tests/__init__.py`

- [ ] **Step 1: Create directories and placeholder files**

Run in the project root (`mastering bitcoin swahili/`):

```powershell
New-Item -ItemType Directory -Force tools, tests, swahili
New-Item -ItemType File -Force tests/__init__.py
New-Item -ItemType File -Force tools/.gitkeep
New-Item -ItemType File -Force swahili/.gitkeep
```

- [ ] **Step 2: Verify structure**

```powershell
Get-ChildItem -Name
```

Expected output includes: `bitcoinbook-third_edition_print1`, `docs`, `swahili`, `tests`, `tools`

- [ ] **Step 3: Commit**

```powershell
git init
git add tools tests swahili docs
git commit -m "chore: scaffold project structure for Swahili translation toolchain"
```

---

## Task 2: Glossary Seed File + Build Script

**Files:**
- Create: `tools/glossary_seed.json`
- Create: `tools/build_glossary.py`
- Create: `tests/test_build_glossary.py`

### Step 1: Write the failing tests

- [ ] Create `tests/test_build_glossary.py`:

```python
import json
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
from build_glossary import extract_index_terms, build_scaffold


def test_extract_index_terms_finds_single_term():
    text = 'Bitcoin((("blockchain", "overview"))) is decentralized.'
    result = extract_index_terms(text)
    assert "blockchain" in result


def test_extract_index_terms_finds_multiple_terms():
    text = '((("mining"))) and ((("wallet"))) are related.'
    result = extract_index_terms(text)
    assert "mining" in result
    assert "wallet" in result


def test_extract_index_terms_empty_text():
    assert extract_index_terms("No index markers here.") == set()


def test_build_scaffold_includes_seed_terms():
    seed = [{"english": "mining", "swahili": "uchimbaji", "type": "translated"}]
    scaffold = build_scaffold(set(), seed)
    assert "mining" in scaffold
    assert "uchimbaji" in scaffold


def test_build_scaffold_marks_missing_translations():
    seed = [{"english": "mempool", "swahili": "", "type": ""}]
    scaffold = build_scaffold(set(), seed)
    assert "[TAFSIRI INAHITAJIKA]" in scaffold


def test_build_scaffold_includes_scanned_terms_not_in_seed():
    seed = []
    scanned = {"orphan_term"}
    scaffold = build_scaffold(scanned, seed)
    assert "orphan_term" in scaffold


def test_build_scaffold_deduplicates_seed_and_scanned():
    seed = [{"english": "block", "swahili": "kizuizi", "type": "translated"}]
    scanned = {"block"}
    scaffold = build_scaffold(scanned, seed)
    assert scaffold.count("block::") == 1
```

- [ ] **Step 2: Run tests to confirm they fail**

```powershell
python -m pytest tests/test_build_glossary.py -v
```

Expected: `ModuleNotFoundError` or `ImportError` — `build_glossary` does not exist yet.

- [ ] **Step 3: Create `tools/glossary_seed.json`**

```json
[
  {"english": "bitcoin",              "swahili": "bitcoini",                    "type": "transliterated"},
  {"english": "blockchain",           "swahili": "mlolongo wa vizuizi",          "type": "translated"},
  {"english": "block",                "swahili": "kizuizi",                     "type": "translated"},
  {"english": "transaction",          "swahili": "muamala",                     "type": "translated"},
  {"english": "wallet",               "swahili": "mkoba",                       "type": "translated"},
  {"english": "mining",               "swahili": "uchimbaji",                   "type": "translated"},
  {"english": "miner",                "swahili": "mchimbaji",                   "type": "translated"},
  {"english": "node",                 "swahili": "nodi",                        "type": "transliterated"},
  {"english": "network",              "swahili": "mtandao",                     "type": "translated"},
  {"english": "private key",          "swahili": "ufunguo wa siri",             "type": "translated"},
  {"english": "public key",           "swahili": "ufunguo wa umma",             "type": "translated"},
  {"english": "address",              "swahili": "anwani",                      "type": "translated"},
  {"english": "hash",                 "swahili": "hashi",                       "type": "transliterated"},
  {"english": "signature",            "swahili": "saini",                       "type": "translated"},
  {"english": "script",               "swahili": "hati",                        "type": "translated"},
  {"english": "fee",                  "swahili": "ada",                         "type": "translated"},
  {"english": "mempool",              "swahili": "hifadhi ya miamala",          "type": "translated"},
  {"english": "confirmation",         "swahili": "uthibitisho",                 "type": "translated"},
  {"english": "proof of work",        "swahili": "uthibitisho wa kazi",         "type": "translated"},
  {"english": "merkle tree",          "swahili": "mti wa merkle",               "type": "translated"},
  {"english": "merkle root",          "swahili": "mzizi wa merkle",             "type": "translated"},
  {"english": "UTXO",                 "swahili": "UTXO",                        "type": "preserved"},
  {"english": "coinbase",             "swahili": "muamala wa asili",            "type": "translated"},
  {"english": "halving",              "swahili": "upunguzaji wa nusu",          "type": "translated"},
  {"english": "difficulty",           "swahili": "ugumu",                       "type": "translated"},
  {"english": "nonce",                "swahili": "nambari ya matumizi mara moja","type": "translated"},
  {"english": "fork",                 "swahili": "tawi",                        "type": "translated"},
  {"english": "soft fork",            "swahili": "tawi laini",                  "type": "translated"},
  {"english": "hard fork",            "swahili": "tawi gumu",                   "type": "translated"},
  {"english": "full node",            "swahili": "nodi kamili",                 "type": "translated"},
  {"english": "peer-to-peer",         "swahili": "rika kwa rika",               "type": "translated"},
  {"english": "key pair",             "swahili": "jozi ya ufunguo",             "type": "translated"},
  {"english": "seed phrase",          "swahili": "maneno ya mbegu",             "type": "translated"},
  {"english": "mnemonic",             "swahili": "mnemoni",                     "type": "transliterated"},
  {"english": "entropy",              "swahili": "nasibu",                      "type": "translated"},
  {"english": "checksum",             "swahili": "ukaguzi wa jumla",            "type": "translated"},
  {"english": "derivation path",      "swahili": "njia ya utokaji",             "type": "translated"},
  {"english": "HD wallet",            "swahili": "mkoba wa kihierarki",         "type": "translated"},
  {"english": "multisig",             "swahili": "saini nyingi",                "type": "translated"},
  {"english": "timelock",             "swahili": "kufunga kwa wakati",          "type": "translated"},
  {"english": "lightning network",    "swahili": "Lightning Network",           "type": "preserved"},
  {"english": "channel",              "swahili": "njia",                        "type": "translated"},
  {"english": "SegWit",               "swahili": "SegWit",                      "type": "preserved"},
  {"english": "Taproot",              "swahili": "Taproot",                     "type": "preserved"},
  {"english": "Tapscript",            "swahili": "Tapscript",                   "type": "preserved"},
  {"english": "PSBT",                 "swahili": "PSBT",                        "type": "preserved"},
  {"english": "BIP",                  "swahili": "BIP",                         "type": "preserved"},
  {"english": "SHA-256",              "swahili": "SHA-256",                     "type": "preserved"},
  {"english": "ECDSA",                "swahili": "ECDSA",                       "type": "preserved"},
  {"english": "Schnorr signature",    "swahili": "saini ya Schnorr",            "type": "translated"},
  {"english": "elliptic curve",       "swahili": "mkondo wa duaradufu",         "type": "translated"},
  {"english": "WIF",                  "swahili": "WIF",                         "type": "preserved"},
  {"english": "scriptPubKey",         "swahili": "scriptPubKey",                "type": "preserved"},
  {"english": "scriptSig",            "swahili": "scriptSig",                   "type": "preserved"},
  {"english": "witness",              "swahili": "shahidi",                     "type": "translated"},
  {"english": "locktime",             "swahili": "muda wa kufunga",             "type": "translated"},
  {"english": "block reward",         "swahili": "tuzo ya kizuizi",             "type": "translated"},
  {"english": "block header",         "swahili": "kichwa cha kizuizi",          "type": "translated"},
  {"english": "target",               "swahili": "lengo",                       "type": "translated"},
  {"english": "timestamp",            "swahili": "muhuri wa wakati",            "type": "translated"},
  {"english": "genesis block",        "swahili": "kizuizi cha mwanzo",          "type": "translated"},
  {"english": "opcode",               "swahili": "opcode",                      "type": "preserved"},
  {"english": "P2PKH",                "swahili": "P2PKH",                       "type": "preserved"},
  {"english": "P2SH",                 "swahili": "P2SH",                        "type": "preserved"},
  {"english": "P2WPKH",               "swahili": "P2WPKH",                      "type": "preserved"},
  {"english": "P2WSH",                "swahili": "P2WSH",                       "type": "preserved"},
  {"english": "P2TR",                 "swahili": "P2TR",                        "type": "preserved"},
  {"english": "RBF",                  "swahili": "RBF",                         "type": "preserved"},
  {"english": "CPFP",                 "swahili": "CPFP",                        "type": "preserved"},
  {"english": "dust",                 "swahili": "vumbi",                       "type": "translated"},
  {"english": "change output",        "swahili": "matokeo ya chenji",           "type": "translated"},
  {"english": "input",                "swahili": "ingizo",                      "type": "translated"},
  {"english": "output",               "swahili": "tokeo",                       "type": "translated"},
  {"english": "SPV",                  "swahili": "SPV",                         "type": "preserved"},
  {"english": "base58",               "swahili": "base58",                      "type": "preserved"},
  {"english": "bech32",               "swahili": "bech32",                      "type": "preserved"},
  {"english": "xpub",                 "swahili": "xpub",                        "type": "preserved"},
  {"english": "xpriv",                "swahili": "xpriv",                       "type": "preserved"},
  {"english": "digital currency",     "swahili": "sarafu ya kidijitali",        "type": "translated"},
  {"english": "decentralized",        "swahili": "iliyosambazwa",               "type": "translated"},
  {"english": "cryptography",         "swahili": "usimbaji fiche",              "type": "translated"},
  {"english": "open source",          "swahili": "chanzo wazi",                 "type": "translated"},
  {"english": "protocol",             "swahili": "itifaki",                     "type": "translated"}
]
```

- [ ] **Step 4: Create `tools/build_glossary.py`**

```python
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
```

- [ ] **Step 5: Run tests to confirm they pass**

```powershell
python -m pytest tests/test_build_glossary.py -v
```

Expected: all 7 tests PASS.

- [ ] **Step 6: Commit**

```powershell
git add tools/glossary_seed.json tools/build_glossary.py tests/test_build_glossary.py
git commit -m "feat: add glossary seed data and build_glossary script"
```

---

## Task 3: Translation Status Tracker

**Files:**
- Create: `tools/translation_status.py`
- Create: `tests/test_translation_status.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_translation_status.py`:

```python
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
from translation_status import get_status, word_count


def test_get_status_returns_missing_for_nonexistent_file(tmp_path):
    assert get_status(tmp_path / "nonexistent.adoc") == "missing"


def test_get_status_returns_draft_for_file_without_header(tmp_path):
    f = tmp_path / "ch01.adoc"
    f.write_text("== Introduction\nSome content.", encoding="utf-8")
    assert get_status(f) == "draft"


def test_get_status_reads_status_from_metadata_header(tmp_path):
    f = tmp_path / "ch01.adoc"
    f.write_text("// status: reviewed\n== Utangulizi\n", encoding="utf-8")
    assert get_status(f) == "reviewed"


def test_get_status_reads_final(tmp_path):
    f = tmp_path / "ch01.adoc"
    f.write_text("// status: final\n", encoding="utf-8")
    assert get_status(f) == "final"


def test_word_count_returns_zero_for_missing_file(tmp_path):
    assert word_count(tmp_path / "missing.adoc") == 0


def test_word_count_counts_prose_words(tmp_path):
    f = tmp_path / "ch01.adoc"
    f.write_text("Hii ni sentensi moja nzuri.", encoding="utf-8")
    assert word_count(f) == 5


def test_word_count_excludes_adoc_anchors(tmp_path):
    f = tmp_path / "ch01.adoc"
    f.write_text("[[ch01_intro]]\n== Utangulizi\nManeno matano ya kweli.", encoding="utf-8")
    result = word_count(f)
    assert result < 10
```

- [ ] **Step 2: Run tests to confirm they fail**

```powershell
python -m pytest tests/test_translation_status.py -v
```

Expected: `ModuleNotFoundError` for `translation_status`.

- [ ] **Step 3: Create `tools/translation_status.py`**

```python
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
```

- [ ] **Step 4: Run tests to confirm they pass**

```powershell
python -m pytest tests/test_translation_status.py -v
```

Expected: all 7 tests PASS.

- [ ] **Step 5: Commit**

```powershell
git add tools/translation_status.py tests/test_translation_status.py
git commit -m "feat: add translation_status progress tracker"
```

---

## Task 4: Glossary Validator

**Files:**
- Create: `tools/validate_glossary.py`
- Create: `tests/test_validate_glossary.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_validate_glossary.py`:

```python
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
from validate_glossary import load_glossary, check_file


SAMPLE_GLOSSARY = """\
[[term-mining]]
mining::
  [type:translated] uchimbaji

[[term-bitcoin]]
bitcoin::
  [type:transliterated] bitcoini

[[term-SHA-256]]
SHA-256::
  [type:preserved] SHA-256
"""


def test_load_glossary_parses_translated_term(tmp_path):
    gfile = tmp_path / "glossary.asciidoc"
    gfile.write_text(SAMPLE_GLOSSARY, encoding="utf-8")
    result = load_glossary(gfile)
    assert "mining" in result
    assert result["mining"]["swahili"] == "uchimbaji"
    assert result["mining"]["type"] == "translated"


def test_load_glossary_parses_preserved_term(tmp_path):
    gfile = tmp_path / "glossary.asciidoc"
    gfile.write_text(SAMPLE_GLOSSARY, encoding="utf-8")
    result = load_glossary(gfile)
    assert "SHA-256" in result
    assert result["SHA-256"]["type"] == "preserved"


def test_check_file_reports_missing_swahili_equivalent(tmp_path):
    gfile = tmp_path / "glossary.asciidoc"
    gfile.write_text(SAMPLE_GLOSSARY, encoding="utf-8")
    glossary = load_glossary(gfile)

    chapter = tmp_path / "ch01.adoc"
    chapter.write_text("The mining process creates new blocks.", encoding="utf-8")
    issues = check_file(chapter, glossary)
    assert any("mining" in issue for issue in issues)


def test_check_file_no_issue_when_swahili_present(tmp_path):
    gfile = tmp_path / "glossary.asciidoc"
    gfile.write_text(SAMPLE_GLOSSARY, encoding="utf-8")
    glossary = load_glossary(gfile)

    chapter = tmp_path / "ch01.adoc"
    chapter.write_text("Uchimbaji (mining) hutengeneza vizuizi.", encoding="utf-8")
    issues = check_file(chapter, glossary)
    assert not any("mining" in issue for issue in issues)


def test_check_file_skips_preserved_terms(tmp_path):
    gfile = tmp_path / "glossary.asciidoc"
    gfile.write_text(SAMPLE_GLOSSARY, encoding="utf-8")
    glossary = load_glossary(gfile)

    chapter = tmp_path / "ch01.adoc"
    chapter.write_text("The hash function SHA-256 is used throughout.", encoding="utf-8")
    issues = check_file(chapter, glossary)
    assert not any("SHA-256" in issue for issue in issues)
```

- [ ] **Step 2: Run tests to confirm they fail**

```powershell
python -m pytest tests/test_validate_glossary.py -v
```

Expected: `ModuleNotFoundError` for `validate_glossary`.

- [ ] **Step 3: Create `tools/validate_glossary.py`**

```python
#!/usr/bin/env python3
"""Detect inconsistent Swahili terminology across translated chapters."""

import re
import sys
from pathlib import Path

SWAHILI_DIR = Path("swahili")
GLOSSARY_FILE = SWAHILI_DIR / "glossary.asciidoc"


def load_glossary(glossary_file: Path) -> dict:
    """Returns {english_term: {swahili, type}}."""
    terms = {}
    text = glossary_file.read_text(encoding="utf-8")
    pattern = r"^([\w][\w\s\-/]+?)::\n\s+\[type:(\w*)\]\s+(.+)$"
    for m in re.finditer(pattern, text, re.MULTILINE):
        english = m.group(1).strip()
        term_type = m.group(2).strip()
        swahili = m.group(3).strip()
        if swahili and swahili != "[TAFSIRI INAHITAJIKA]":
            terms[english] = {"swahili": swahili, "type": term_type}
    return terms


def check_file(filepath: Path, glossary: dict) -> list:
    issues = []
    text = filepath.read_text(encoding="utf-8")
    for english, data in glossary.items():
        if data["type"] == "preserved":
            continue
        expected_swahili = data["swahili"]
        if re.search(rf"\b{re.escape(english)}\b", text, re.IGNORECASE):
            if not re.search(re.escape(expected_swahili), text, re.IGNORECASE):
                issues.append(
                    f"  '{english}' found without Swahili equivalent '{expected_swahili}'"
                )
    return issues


def main():
    if not GLOSSARY_FILE.exists():
        print(f"ERROR: {GLOSSARY_FILE} not found. Run Session 1 first.")
        sys.exit(1)

    glossary = load_glossary(GLOSSARY_FILE)
    print(f"Loaded {len(glossary)} glossary terms (excluding preserved)")

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
```

- [ ] **Step 4: Run tests to confirm they pass**

```powershell
python -m pytest tests/test_validate_glossary.py -v
```

Expected: all 5 tests PASS.

- [ ] **Step 5: Commit**

```powershell
git add tools/validate_glossary.py tests/test_validate_glossary.py
git commit -m "feat: add validate_glossary consistency checker"
```

---

## Task 5: AsciiDoc Structure Validator

**Files:**
- Create: `tools/validate_adoc.py`
- Create: `tests/test_validate_adoc.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_validate_adoc.py`:

```python
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
from validate_adoc import check_anchors, check_blocks, check_metadata_header

VALID_HEADER = """\
// TRANSLATION METADATA
// source: ch01_intro.adoc
// translator: Juma Mwanga
// date: 2026-05-26
// status: draft
// glossary-version: 1.0
"""


def test_check_anchors_passes_for_valid_xref():
    text = "[[ch01_intro]]\n== Utangulizi\nAngalia <<ch02_overview>>.\n[[ch02_overview]]\n== Muhtasari"
    assert check_anchors(text) == []


def test_check_anchors_fails_for_broken_xref():
    text = "[[ch01_intro]]\n== Utangulizi\nAngalia <<ch99_missing>>."
    issues = check_anchors(text)
    assert any("ch99_missing" in i for i in issues)


def test_check_blocks_passes_for_balanced_delimiters():
    text = "====\nNote here.\n===="
    assert check_blocks(text) == []


def test_check_blocks_fails_for_unclosed_tip_block():
    text = "====\nNote here without closing."
    issues = check_blocks(text)
    assert any("====" in i for i in issues)


def test_check_blocks_passes_for_balanced_code_block():
    text = "----\ncode here\n----"
    assert check_blocks(text) == []


def test_check_metadata_header_passes_complete_header():
    assert check_metadata_header(VALID_HEADER) == []


def test_check_metadata_header_fails_missing_field():
    text = "// source: ch01_intro.adoc\n// translator: Juma\n"
    issues = check_metadata_header(text)
    assert any("date" in i for i in issues)
    assert any("status" in i for i in issues)
    assert any("glossary-version" in i for i in issues)
```

- [ ] **Step 2: Run tests to confirm they fail**

```powershell
python -m pytest tests/test_validate_adoc.py -v
```

Expected: `ModuleNotFoundError` for `validate_adoc`.

- [ ] **Step 3: Create `tools/validate_adoc.py`**

```python
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

BLOCK_DELIMITERS = ("====", "----", "****", "____", "....")


def check_metadata_header(text: str) -> list:
    return [
        f"  Missing header field: {field}"
        for field in REQUIRED_HEADER_FIELDS
        if field not in text
    ]


def check_anchors(text: str) -> list:
    anchors = set(re.findall(r"\[\[([^\]]+)\]\]", text))
    xrefs = re.findall(r"<<([^,>\s]+)[,>]", text)
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
```

- [ ] **Step 4: Run all tests**

```powershell
python -m pytest tests/ -v
```

Expected: all 27 tests PASS across all four test files.

- [ ] **Step 5: Commit**

```powershell
git add tools/validate_adoc.py tests/test_validate_adoc.py
git commit -m "feat: add validate_adoc AsciiDoc structure checker"
```

---

## Task 6: Glossary Bootstrap (Session 1)

**Files:**
- Create: `swahili/glossary.asciidoc`

- [ ] **Step 1: Run the glossary builder**

From the project root:

```powershell
python tools/build_glossary.py
```

Expected output:
```
Scaffold written to swahili/glossary_scaffold.adoc
Scanned terms: <N> scanned, Seed terms: 80
```

- [ ] **Step 2: Review and complete the scaffold**

Open `swahili/glossary_scaffold.adoc`. For every entry marked `[TAFSIRI INAHITAJIKA]`, supply the Swahili translation and set the `type` field to `translated`, `transliterated`, or `preserved`. Use the seed file entries as references. For any term where you are uncertain, default to `preserved` and document your reasoning in a comment line starting with `// NOTE:`.

- [ ] **Step 3: Save as the authoritative glossary**

Once all entries are filled in, save the file as `swahili/glossary.asciidoc` (keep the scaffold for reference):

```powershell
Copy-Item swahili/glossary_scaffold.adoc swahili/glossary.asciidoc
```

Then edit `swahili/glossary.asciidoc` to update the metadata header:
```
// status: draft
// glossary-version: 1.0
```

- [ ] **Step 4: Validate the glossary file**

```powershell
python tools/validate_adoc.py swahili/glossary.asciidoc
```

Expected: `OK: glossary.asciidoc passes all structural checks.`

- [ ] **Step 5: Check progress table**

```powershell
python tools/translation_status.py
```

Expected: `glossary.asciidoc` shows `[~] draft`.

- [ ] **Step 6: Commit**

```powershell
git add swahili/glossary.asciidoc swahili/glossary_scaffold.adoc
git commit -m "feat: add Swahili-English master glossary (v1.0)"
```

---

## Tasks 7–26: Translation Sessions

Each task below follows the identical 5-step workflow. The file to translate is specified per task.

**Standard translation workflow (repeat for every task below):**

- [ ] **Step A: Check progress**
  ```powershell
  python tools/translation_status.py
  ```
  Confirm the target file shows `[ ] missing`.

- [ ] **Step B: Translate the file**
  Open `bitcoinbook-third_edition_print1/<filename>` and `swahili/glossary.asciidoc` side by side. Translate all prose into Standard Kiswahili (Kiswahili Sanifu), applying these rules:
  - Add translation metadata header at the top of the file (copy template below)
  - First occurrence of a Bitcoin term: `Swahili term (English term)` per the glossary
  - Subsequent occurrences: Swahili term only
  - Preserve all AsciiDoc syntax: `[[anchors]]`, `<<xrefs>>`, `[TIP]`, `====`, `----`, `(((...)))`
  - Preserve all code blocks (`----` delimited) untranslated
  - Preserve all proper nouns, person names, protocol names
  - Index markers: duplicate to include both English and Swahili, e.g. `((("mining","uchimbaji")))`

  **Metadata header template:**
  ```asciidoc
  // TRANSLATION METADATA
  // source: <original_filename>
  // translator: <your name>
  // date: <YYYY-MM-DD>
  // status: draft
  // glossary-version: 1.0
  ```

- [ ] **Step C: Validate structure**
  ```powershell
  python tools/validate_adoc.py swahili/<filename>
  ```
  Fix any reported issues before continuing.

- [ ] **Step D: Commit**
  ```powershell
  git add swahili/<filename>
  git commit -m "translate: <filename> to Swahili (draft)"
  ```

- [ ] **Step E: Every 4th chapter — run glossary consistency check**
  ```powershell
  python tools/validate_glossary.py
  ```
  Fix any inconsistencies, then commit the corrections.

---

### Task 7: Translate `preface.adoc`
Apply workflow steps A–D to `preface.adoc`.

### Task 8: Translate `ch01_intro.adoc`
Apply workflow steps A–D to `ch01_intro.adoc`.

### Task 9: Translate `ch02_overview.adoc`
Apply workflow steps A–D to `ch02_overview.adoc`.

### Task 10: Translate `ch03_bitcoin-core.adoc`
Apply workflow steps A–D to `ch03_bitcoin-core.adoc`.
**After this task:** Run Step E (glossary consistency check across ch01–ch03).

### Task 11: Translate `ch04_keys.adoc`
Apply workflow steps A–D to `ch04_keys.adoc`.
Note: This chapter is dense with cryptographic terms. Cross-check every key/signature term carefully against `glossary.asciidoc`.

### Task 12: Translate `ch05_wallets.adoc`
Apply workflow steps A–D to `ch05_wallets.adoc`.

### Task 13: Translate `ch06_transactions.adoc`
Apply workflow steps A–D to `ch06_transactions.adoc`.

### Task 14: Translate `ch07_authorization-authentication.adoc`
Apply workflow steps A–D to `ch07_authorization-authentication.adoc`.
**After this task:** Run Step E (glossary consistency check across ch04–ch07).

### Task 15: Translate `ch08_signatures.adoc`
Apply workflow steps A–D to `ch08_signatures.adoc`.

### Task 16: Translate `ch09_fees.adoc`
Apply workflow steps A–D to `ch09_fees.adoc`.

### Task 17: Translate `ch10_network.adoc`
Apply workflow steps A–D to `ch10_network.adoc`.

### Task 18: Translate `ch11_blockchain.adoc`
Apply workflow steps A–D to `ch11_blockchain.adoc`.
**After this task:** Run Step E (glossary consistency check across ch08–ch11).

### Task 19: Translate `ch12_mining.adoc`
Apply workflow steps A–D to `ch12_mining.adoc`.

### Task 20: Translate `ch13_security.adoc`
Apply workflow steps A–D to `ch13_security.adoc`.

### Task 21: Translate `ch14_applications.adoc`
Apply workflow steps A–D to `ch14_applications.adoc`.
**After this task:** Run Step E (glossary consistency check across ch12–ch14).

### Task 22: Translate `appa_whitepaper.adoc`
Apply workflow steps A–D to `appa_whitepaper.adoc`.
Note: This appendix contains the original Satoshi Nakamoto white paper. The Bitcoin white paper in Swahili PDF already exists in this project — use it as a reference for established Swahili terminology.

### Task 23: Translate `appb_errata.adoc`
Apply workflow steps A–D to `appb_errata.adoc`.

### Task 24: Translate `appc_bips.adoc`
Apply workflow steps A–D to `appc_bips.adoc`.

### Task 25: Translate `tapscript.asciidoc`
Apply workflow steps A–D to `tapscript.asciidoc`.

---

## Task 26: Final Assembly and Validation

**Files:**
- Create: `swahili/book.adoc`

- [ ] **Step 1: Run full glossary validation across all chapters**

```powershell
python tools/validate_glossary.py
```

Fix every reported inconsistency. Commit corrections:

```powershell
git add swahili/
git commit -m "fix: resolve glossary consistency issues in final pass"
```

- [ ] **Step 2: Run structural validation on all translated files**

```powershell
Get-ChildItem swahili -Filter "*.adoc" | ForEach-Object {
    python tools/validate_adoc.py $_.FullName
}
```

Fix all reported issues. Commit any fixes.

- [ ] **Step 3: Create `swahili/book.adoc`**

Open `bitcoinbook-third_edition_print1/book.adoc` and create `swahili/book.adoc` by updating all `include::` paths to point at the `swahili/` files:

```asciidoc
// TRANSLATION METADATA
// source: book.adoc
// translator: <your name>
// date: <YYYY-MM-DD>
// status: final
// glossary-version: 1.0

= Kumudu Bitcoin: Kupanga Blockchain Wazi
Andreas M. Antonopoulos na David Harding
:doctype: book
:toc:

include::preface.adoc[]
include::ch01_intro.adoc[]
include::ch02_overview.adoc[]
include::ch03_bitcoin-core.adoc[]
include::ch04_keys.adoc[]
include::ch05_wallets.adoc[]
include::ch06_transactions.adoc[]
include::ch07_authorization-authentication.adoc[]
include::ch08_signatures.adoc[]
include::ch09_fees.adoc[]
include::ch10_network.adoc[]
include::ch11_blockchain.adoc[]
include::ch12_mining.adoc[]
include::ch13_security.adoc[]
include::ch14_applications.adoc[]
include::appa_whitepaper.adoc[]
include::appb_errata.adoc[]
include::appc_bips.adoc[]
include::tapscript.asciidoc[]
include::glossary.asciidoc[]
```

- [ ] **Step 4: Run final progress check**

```powershell
python tools/translation_status.py
```

Expected: all 20 files show `[~]` draft or better. No `[ ]` missing entries.

- [ ] **Step 5: Final commit**

```powershell
git add swahili/book.adoc
git commit -m "feat: complete Swahili translation assembly — all chapters draft"
```

---

## Attribution Notice

Every compiled output must carry this attribution in the front matter:

> *Mastering Bitcoin: Programming the Open Blockchain* (Toleo la 3) na Andreas M. Antonopoulos na David Harding. Tafsiri ya Kiswahili na [jina la mtafsiri]. Imechapishwa chini ya leseni ya Creative Commons Attribution-ShareAlike 4.0 International (CC-BY-SA 4.0). Chanzo: https://github.com/bitcoinbook/bitcoinbook
