"""Unit tests for the pure/testable helpers in src/app_ui.py.

Only the plain functions are tested here (html/update builders) — the actual
gr.Blocks wiring is exercised by hand in the live demo, not by these tests.
Run: pytest (from repo root)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import app_ui  # noqa: E402


class TestStepDotsHtml:
    def test_marks_the_active_screen_with_the_primary_color(self):
        html = app_ui._step_dots_html("review")

        assert html.count("var(--lk-primary)") == 3  # review + the 2 steps before it
        assert "var(--lk-border)" in html  # the remaining (future) step

    def test_first_screen_has_only_one_active_dot(self):
        html = app_ui._step_dots_html("select")

        assert html.count("var(--lk-primary)") == 1

    def test_last_screen_has_every_dot_active(self):
        html = app_ui._step_dots_html("download")
        steps_section = html.split('<div class="lk-steps">')[1]

        assert html.count("var(--lk-primary)") == len(app_ui.SCREENS)
        assert "var(--lk-border)" not in steps_section

    def test_includes_the_logo_and_app_name(self):
        html = app_ui._step_dots_html("select")

        assert "Feature Launch Kit" in html
        assert str(app_ui.LOGO_PATH) in html


class TestStatusHtml:
    def test_shows_spinner_when_not_done(self):
        html = app_ui._status_html("Loading...", False, 40)

        assert "lk-spinner" in html
        assert "lk-check" not in html
        assert "width:40%;" in html

    def test_shows_checkmark_when_done(self):
        html = app_ui._status_html("Done", True, 100)

        assert "lk-check" in html
        assert "lk-spinner" not in html

    def test_escapes_html_in_status_text(self):
        html = app_ui._status_html("<script>alert(1)</script>", False, 0)

        assert "<script>" not in html
        assert "&lt;script&gt;" in html


class TestBoxUpdates:
    def test_visible_and_populated_for_keys_present_in_content(self):
        content = {"email": "hello world"}

        updates = app_ui._box_updates(content)

        # Two gr.update() entries per key in SECTION_LABELS, in that fixed order.
        assert len(updates) == 2 * len(app_ui.SECTION_LABELS)

    def test_hidden_and_empty_for_keys_missing_from_content(self):
        content = {}  # nothing generated

        updates = app_ui._box_updates(content)

        # With no content, no box should be marked visible.
        visibility_updates = updates[0::2]
        assert all(u.get("visible") is False for u in visibility_updates)

    def test_output_order_matches_section_labels_order(self):
        content = {key: f"text for {key}" for key in app_ui.SECTION_LABELS}

        updates = app_ui._box_updates(content)
        values = [u.get("value") for u in updates[1::2]]

        assert values == [f"text for {key}" for key in app_ui.SECTION_LABELS]


class TestScopeLabelMapping:
    def test_scope_choices_and_scope_by_label_are_consistent(self):
        for label in app_ui.SCOPE_CHOICES:
            assert label in app_ui.SCOPE_BY_LABEL

    def test_every_scope_key_has_a_human_label(self):
        for scope_key in app_ui.SCOPE_BY_LABEL.values():
            assert scope_key in ("all", "marketing", "customer_success", "sales")
