import sys
from pathlib import Path

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


def test_check_file_ignores_terms_in_code_blocks(tmp_path):
    gfile = tmp_path / "glossary.asciidoc"
    gfile.write_text(SAMPLE_GLOSSARY, encoding="utf-8")
    glossary = load_glossary(gfile)

    chapter = tmp_path / "ch01.adoc"
    # 'mining' appears only inside a code block — should not flag
    chapter.write_text(
        "Prose yote ipo hapa.\n\n----\n# mining loop\nfor i in range(10):\n    pass\n----\n",
        encoding="utf-8",
    )
    issues = check_file(chapter, glossary)
    assert not any("mining" in issue for issue in issues)


def test_check_file_no_issue_when_term_absent(tmp_path):
    gfile = tmp_path / "glossary.asciidoc"
    gfile.write_text(SAMPLE_GLOSSARY, encoding="utf-8")
    glossary = load_glossary(gfile)

    chapter = tmp_path / "ch01.adoc"
    chapter.write_text("Hii ni maelezo ya kawaida bila maneno maalum.", encoding="utf-8")
    issues = check_file(chapter, glossary)
    assert issues == []


def test_load_glossary_skips_placeholder_entries(tmp_path):
    glossary_text = "[[term-foo]]\nfoo::\n  [type:translated] [TAFSIRI INAHITAJIKA]\n"
    gfile = tmp_path / "glossary.asciidoc"
    gfile.write_text(glossary_text, encoding="utf-8")
    result = load_glossary(gfile)
    assert "foo" not in result
