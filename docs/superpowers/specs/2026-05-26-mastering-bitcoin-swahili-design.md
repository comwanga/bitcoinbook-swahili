---
name: mastering-bitcoin-swahili-translation
description: Design spec for translating Mastering Bitcoin 3rd Edition into Swahili using a scripted workflow + interactive translation approach
metadata:
  type: project
---

# Mastering Bitcoin — Swahili Translation Project
**Date:** 2026-05-26
**Status:** Approved for implementation

---

## Goal

Produce a complete, high-quality Swahili translation of *Mastering Bitcoin: Programming the Open Blockchain* (3rd Edition) by Andreas M. Antonopoulos & David Harding. The mission is to make Bitcoin technical knowledge accessible to Swahili-speaking communities across East and Central Africa.

---

## Copyright

The 3rd edition is currently licensed under **CC-BY-NC-ND**. The LICENSE file states the authors intended to re-release under **CC-BY-SA** after one year of publication (2023). As of 2026 that window has passed.

**Action required before publishing:** Confirm on the official GitHub repo (bitcoinbook/bitcoinbook) or by contacting the authors that the CC-BY-SA license is now active. All translated output must carry attribution per CC-BY-SA requirements.

---

## Source Material

- **Location:** `bitcoinbook-third_edition_print1/`
- **Format:** AsciiDoc (`.adoc` / `.asciidoc`)
- **Files to translate:** 20 files
  - `preface.adoc`
  - `ch01_intro.adoc` through `ch14_applications.adoc`
  - `appa_whitepaper.adoc`, `appb_errata.adoc`, `appc_bips.adoc`
  - `tapscript.asciidoc`
  - `glossary.asciidoc`
- **`book.adoc`:** The master include file that references all chapter files. The Swahili version must update all `include::` directives to point at `swahili/` chapter paths. This is done in Session 21 once all chapters are translated.
- **Do not translate:** `code/`, `draft_images/`, HTML files, `.gitignore`, `LICENSE`, `atlas.json`

---

## Translation Decisions

### Terminology Strategy: Hybrid + Glossary
- All prose is translated into Swahili (Standard Kiswahili Sanifu)
- On **first occurrence** of a Bitcoin technical term: `Swahili term (English term)` — e.g., *uchimbaji (mining)*
- Subsequent occurrences: Swahili term only
- A master `glossary.asciidoc` in the output directory is the single source of truth for all term translations

### Term Classification
Every glossary entry is tagged with one of three types:

| Type | Meaning | Example |
|---|---|---|
| `translated` | Has a Swahili equivalent | _uchimbaji_ (mining) |
| `transliterated` | Adapted phonetically | _bitcoini_ (bitcoin) |
| `preserved` | Kept in English by design | SHA-256, SegWit, Taproot |

### What Is Never Translated
- Code blocks (`----` delimited)
- AsciiDoc structural syntax: anchors `[[...]]`, cross-references `<<...>>`, attribute entries
- Proper nouns, person names, company names, protocol names (e.g., Lightning Network)
- Index markers `((("term")))` — duplicated to include both English and Swahili terms

### What May Optionally Be Translated
- Inline code comments (`#`, `//`) within code blocks

---

## Output Structure

```
mastering bitcoin swahili/
├── bitcoinbook-third_edition_print1/   ← source (never modified)
├── swahili/                            ← all translated output
│   ├── book.adoc
│   ├── preface.adoc
│   ├── ch01_intro.adoc
│   ├── ch02_overview.adoc
│   ├── ch03_bitcoin-core.adoc
│   ├── ch04_keys.adoc
│   ├── ch05_wallets.adoc
│   ├── ch06_transactions.adoc
│   ├── ch07_authorization-authentication.adoc
│   ├── ch08_signatures.adoc
│   ├── ch09_fees.adoc
│   ├── ch10_network.adoc
│   ├── ch11_blockchain.adoc
│   ├── ch12_mining.adoc
│   ├── ch13_security.adoc
│   ├── ch14_applications.adoc
│   ├── appa_whitepaper.adoc
│   ├── appb_errata.adoc
│   ├── appc_bips.adoc
│   ├── tapscript.asciidoc
│   └── glossary.asciidoc              ← master Swahili-English glossary
└── tools/
    ├── build_glossary.py              ← scans source, extracts terms into scaffold
    ├── translation_status.py          ← per-file progress table
    ├── validate_glossary.py           ← detects inconsistent term usage across chapters
    ├── validate_adoc.py               ← Asciidoctor dry-run validation per chapter
    └── glossary_seed.json             ← curated ~80 core Bitcoin term list
```

---

## Toolchain

### `build_glossary.py`
- Scans all source `.adoc` files for AsciiDoc index markers `((("term")))`
- Augments with terms from `glossary_seed.json`
- Outputs `swahili/glossary_scaffold.adoc` — pre-populated with English terms, blank Swahili fields and empty `type` tags
- Run once to bootstrap; human fills in Swahili translations and renames/copies file to `swahili/glossary.asciidoc` (the authoritative file). The scaffold is an intermediate artifact only — `glossary.asciidoc` is what all other scripts reference

### `glossary_seed.json`
Curated list of ~80 core Bitcoin/cryptography terms including: blockchain, mining, wallet, private key, public key, hash, node, mempool, transaction, signature, script, taproot, segwit, lightning network, nonce, difficulty, merkle tree, UTXO, coinbase, halving, and others.

### `translation_status.py`
- Compares `swahili/` against source directory
- Prints a table: filename | status (missing / draft / reviewed / final) | word count
- Status is read from the metadata header of each translated file

### `validate_glossary.py`
- Loads `glossary.asciidoc` to build a term → Swahili mapping
- Scans all translated `.adoc` files for occurrences of English terms that should have Swahili equivalents
- Reports: inconsistent translations, missing first-occurrence parenthetical, preserved terms used without classification

### `validate_adoc.py`
- Runs `asciidoctor --dry-run` (or equivalent structural check) on a given translated file
- Reports broken cross-references `<<...>>`, malformed blocks, missing anchors
- Called at the end of every translation session before closing

---

## Translation Metadata Header

Every translated `.adoc` file begins with:

```asciidoc
// TRANSLATION METADATA
// source: <original filename>
// translator: <name or handle>
// date: YYYY-MM-DD
// status: draft | reviewed | final
// glossary-version: <version number>
```

---

## Session Workflow

### Session 1 — Glossary Bootstrap
1. Run `build_glossary.py` → generates `glossary_scaffold.adoc`
2. Manually fill in Swahili translations and type classifications for all ~80+ terms
3. Save as `swahili/glossary.asciidoc` — this is now authoritative
4. Tag glossary-version as `1.0`

### Sessions 2–21 — Chapter-by-Chapter Translation
For each session:
1. Run `translation_status.py` → identify next file in order
2. Open source file alongside `swahili/glossary.asciidoc`
3. Translate interactively, enforcing all translation rules
4. Add metadata header with current date and `status: draft`
5. Write output to `swahili/<filename>`
6. Run `validate_adoc.py` on the new file — fix all errors before closing
7. Every 3–4 chapters: run `validate_glossary.py` across all completed files

### Translation Order
| Session | File |
|---|---|
| 1 | `glossary.asciidoc` (bootstrap) |
| 2 | `preface.adoc` |
| 3 | `ch01_intro.adoc` |
| 4 | `ch02_overview.adoc` |
| 5 | `ch03_bitcoin-core.adoc` |
| 6 | `ch04_keys.adoc` |
| 7 | `ch05_wallets.adoc` |
| 8 | `ch06_transactions.adoc` |
| 9 | `ch07_authorization-authentication.adoc` |
| 10 | `ch08_signatures.adoc` |
| 11 | `ch09_fees.adoc` |
| 12 | `ch10_network.adoc` |
| 13 | `ch11_blockchain.adoc` |
| 14 | `ch12_mining.adoc` |
| 15 | `ch13_security.adoc` |
| 16 | `ch14_applications.adoc` |
| 17 | `appa_whitepaper.adoc` |
| 18 | `appb_errata.adoc` |
| 19 | `appc_bips.adoc` |
| 20 | `tapscript.asciidoc` |
| 21 | Final validation pass + `book.adoc` update |

---

## Quality Gates

| Gate | When | Tool |
|---|---|---|
| AsciiDoc structure valid | End of every session | `validate_adoc.py` |
| Glossary consistency | Every 3–4 chapters | `validate_glossary.py` |
| Progress check | Start of every session | `translation_status.py` |
| Final compile | Session 21 | `asciidoctor` full build |

---

## Attribution (CC-BY-SA)

Every translated file and the compiled output must carry:

> *Mastering Bitcoin: Programming the Open Blockchain* (3rd Edition) na Andreas M. Antonopoulos na David Harding. Tafsiri ya Kiswahili na [translator name(s)]. Imechapishwa chini ya leseni ya Creative Commons Attribution-ShareAlike 4.0 International (CC-BY-SA 4.0).

---

## Out of Scope

- Translation of `code/` Python files
- Translation of image captions embedded in PNG files
- Translation of `contrib/` directory
- Commercial publishing decisions
- Human peer-review scheduling (beyond the workflow described)
