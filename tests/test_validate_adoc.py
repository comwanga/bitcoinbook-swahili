import sys
from pathlib import Path

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


def test_check_anchors_ignores_xrefs_in_code_blocks():
    # xref inside ---- block should not be flagged as broken
    text = "[[real_anchor]]\n== Title\n\n----\nSee <<fake_missing>>.\n----\n"
    assert check_anchors(text) == []


def test_check_anchors_deduplicates_broken_xrefs():
    # same broken xref appearing twice should produce only one issue
    text = "See <<gone>> and also <<gone>> again."
    issues = check_anchors(text)
    assert len([i for i in issues if "gone" in i]) == 1


def test_check_metadata_header_passes_with_blank_preamble_line():
    # a blank line before the comment block should still be found within 20 lines
    header = "\n" + VALID_HEADER
    assert check_metadata_header(header) == []


def test_check_anchors_handles_xref_with_title():
    # <<anchor,Title>> format should resolve if anchor exists
    text = "[[target]]\n== Section\nSee <<target,Click here>>."
    assert check_anchors(text) == []
