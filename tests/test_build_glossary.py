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


def test_extract_index_terms_ignores_partial_markers():
    text = 'See ((("incomplete" for details.'  # no closing )))
    result = extract_index_terms(text)
    assert result == set()


def test_build_scaffold_anchor_strips_parentheses():
    seed = [{"english": "pay-to-script-hash (P2SH)", "swahili": "P2SH", "type": "preserved"}]
    scaffold = build_scaffold(set(), seed)
    assert "(P2SH)" not in scaffold.split("[[")[1].split("]]")[0]  # no parens in anchor


def test_build_scaffold_no_duplicate_for_case_variant():
    seed = [{"english": "UTXO", "swahili": "UTXO", "type": "preserved"}]
    scanned = {"utxo"}
    scaffold = build_scaffold(scanned, seed)
    assert scaffold.count("utxo::") + scaffold.count("UTXO::") == 1
