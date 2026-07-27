"""
content_pipeline.py — end-to-end generation pipeline (WBS 5.3).

Loads knowledge-base context, runs a prompt template through the LLM client,
and writes the result to output/. Each Must gets one generate_* function
following the same pattern.

Implemented: M3 (sales one-pager).
Run:  python -m src.content_pipeline    (from repo root)
"""

from __future__ import annotations

from pathlib import Path

from src.llm_integration import LLMClient
from src.prompt_templates import build_sales_one_pager_prompt

# --- Paths (relative to repo root; run from there) ---
KB = Path("knowledge_base")
PRIMARY = KB / "primary"
SECONDARY = KB / "secondary"
OUTPUT_DIR = Path("output")


def _read(path: Path) -> str:
    """Read a knowledge-base markdown file as UTF-8."""
    return path.read_text(encoding="utf-8")


def _write_output(filename: str, text: str) -> Path:
    """Write generated content to output/<filename> and return the path."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / filename
    out_path.write_text(text, encoding="utf-8")
    return out_path


def generate_sales_one_pager(client: LLMClient | None = None) -> Path:
    """Generate the sales one-pager (Must M3) and write it to output/."""
    client = client or LLMClient()

    system, user = build_sales_one_pager_prompt(
        feature_context=_read(PRIMARY / "feature_brief.md"),
        brand_context=_read(PRIMARY / "brand_voice.md"),
        research_context=_read(SECONDARY / "sales_enablement_kit.md"),
    )

    result = client.generate(system, user)
    out_path = _write_output("sales_one_pager.txt", result.text)
    print(f"[M3] sales one-pager -> {out_path}  (via {result.provider} / {result.model})")
    return out_path


# --- Extension point for teammates (templates M1/M2 not written yet) ---
# def generate_marketing_email(client=None) -> Path:   # M1
#     system, user = build_marketing_email_prompt(...)
#     return _write_output("marketing_email.txt", client.generate(system, user).text)
#
# def generate_user_guide(client=None) -> Path:        # M2
#     system, user = build_user_guide_prompt(...)
#     return _write_output("user_guide.txt", client.generate(system, user).text)


def main() -> None:
    """Run all implemented generators, reusing one client across outputs."""
    client = LLMClient()
    generate_sales_one_pager(client)


if __name__ == "__main__":
    main()