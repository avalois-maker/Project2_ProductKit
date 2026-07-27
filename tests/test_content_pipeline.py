"""Unit tests for src/content_pipeline.py.

Run: pytest (from repo root)
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import content_pipeline as cp  # noqa: E402


class TestLoadFolder:
    def test_concatenates_markdown_files_sorted_and_labeled(self, tmp_path):
        (tmp_path / "b.md").write_text("second", encoding="utf-8")
        (tmp_path / "a.md").write_text("first", encoding="utf-8")

        result = cp._load_folder(tmp_path)

        assert result.index("a.md") < result.index("b.md")
        assert "## a.md\nfirst" in result
        assert "## b.md\nsecond" in result

    def test_skips_non_markdown_files(self, tmp_path):
        (tmp_path / "notes.md").write_text("keep me", encoding="utf-8")
        (tmp_path / "brand.pdf").write_bytes(b"%PDF-1.4 fake")

        result = cp._load_folder(tmp_path)

        assert "keep me" in result
        assert "brand.pdf" not in result

    def test_skips_subfolders(self, tmp_path):
        (tmp_path / "top.md").write_text("top level", encoding="utf-8")
        sub = tmp_path / "past_content"
        sub.mkdir()
        (sub / "old.md").write_text("should not appear", encoding="utf-8")

        result = cp._load_folder(tmp_path)

        assert "top level" in result
        assert "should not appear" not in result

    def test_missing_folder_returns_empty_string(self, tmp_path):
        missing = tmp_path / "does_not_exist"

        assert cp._load_folder(missing) == ""

    def test_empty_folder_returns_empty_string(self, tmp_path):
        assert cp._load_folder(tmp_path) == ""


class TestListReleases:
    def test_returns_current_release_when_product_has_markdown(self, monkeypatch, tmp_path):
        (tmp_path / "feature_brief.md").write_text("...", encoding="utf-8")
        monkeypatch.setattr(cp, "PRODUCT", tmp_path)

        assert cp.list_releases() == [cp.CURRENT_RELEASE]

    def test_returns_empty_list_when_product_folder_missing(self, monkeypatch, tmp_path):
        monkeypatch.setattr(cp, "PRODUCT", tmp_path / "missing")

        assert cp.list_releases() == []

    def test_returns_empty_list_when_product_folder_has_no_markdown(self, monkeypatch, tmp_path):
        (tmp_path / "notes.txt").write_text("not markdown", encoding="utf-8")
        monkeypatch.setattr(cp, "PRODUCT", tmp_path)

        assert cp.list_releases() == []


class TestGenerateKitScopeValidation:
    def test_rejects_unknown_scope(self):
        with pytest.raises(ValueError, match="scope must be one of"):
            cp.generate_kit("any-release", "not-a-real-scope")

    @pytest.mark.parametrize("scope", ["all", "marketing", "customer_success", "sales"])
    def test_accepts_every_known_scope(self, monkeypatch, scope):
        # Stub out the real generators so this test never calls the LLM.
        fake_path = type("FakePath", (), {"read_text": lambda self, encoding=None: "stub text"})()
        monkeypatch.setitem(
            cp._SCOPE_GENERATORS, scope,
            [(key, lambda client: fake_path) for key, _ in cp._SCOPE_GENERATORS[scope]],
        )
        monkeypatch.setattr(cp, "LLMClient", lambda **kwargs: object())

        result = cp.generate_kit("any-release", scope)

        expected_keys = {key for key, _ in cp._SCOPE_GENERATORS[scope]}
        assert set(result.keys()) == expected_keys
        assert all(value == "stub text" for value in result.values())


class TestScopeGeneratorsMapping:
    def test_all_scope_is_union_of_the_three_named_scopes(self):
        combined = (
            cp._SCOPE_GENERATORS["marketing"]
            + cp._SCOPE_GENERATORS["customer_success"]
            + cp._SCOPE_GENERATORS["sales"]
        )
        assert cp._SCOPE_GENERATORS["all"] == combined

    def test_every_scope_maps_to_a_known_output_key(self):
        known_keys = {"email", "guide", "onepager"}
        for scope in cp.SCOPES:
            keys = {key for key, _ in cp._SCOPE_GENERATORS[scope]}
            assert keys <= known_keys
