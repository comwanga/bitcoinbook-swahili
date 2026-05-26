import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
from translation_status import get_status, word_count  # noqa: E402


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
    f.write_text(
        "[[ch01_intro]]\n== Utangulizi\nManeno matano ya kweli.",
        encoding="utf-8",
    )
    result = word_count(f)
    assert result <= 6  # anchors stripped; heading text may remain


def test_get_status_ignores_status_in_code_block(tmp_path):
    f = tmp_path / "ch01.adoc"
    # status: active appears deep in a code listing, not in the header
    content = "== Utangulizi\n\n" + ("line\n" * 20) + "// status: active\n"
    f.write_text(content, encoding="utf-8")
    assert get_status(f) == "draft"
