"""
content_pipeline.py — end-to-end generation pipeline (WBS 5.3).

Loads knowledge-base context + a markdown prompt spec, runs it through the LLM
client, and writes each output to output/.

Implemented: M1 (marketing kit), M2 (user guide), M3 (sales one-pager).
Run:  python -m src.content_pipeline      (from repo root)
"""

from __future__ import annotations

from pathlib import Path

from src.llm_integration import LLMClient
from src.prompt_templates import build_prompt_from_spec

# ---------------------------------------------------------------------------
# PATHS — adjust these if your folder names differ. This is the only section
# you should need to touch.
# ---------------------------------------------------------------------------
KB = Path("knowledge_base")
PRODUCT = KB / "product"        # PRD / release docs
PRIMARY = KB / "primary"        # company / brand / product info
SECONDARY = KB / "secondary"    # communication / tone / best practices

TEMPLATES = Path("templates")   # prompt spec .md files live here
OUTPUT_DIR = Path("output")

# Map each output to (spec file, output filename, Must ID)
SPEC_MARKETING = TEMPLATES / "marketing_email.md"
SPEC_USER_GUIDE = TEMPLATES / "customer_guide.md"
SPEC_SALES = TEMPLATES / "sales_onepager.md"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _read(path: Path) -> str:
    """Read a single file as UTF-8."""
    return path.read_text(encoding="utf-8")


def _load_folder(folder: Path) -> str:
    """
    Concatenate every top-level .md file in a folder (sorted, labeled).
    Non-recursive on purpose: skips subfolders (e.g. past_content/) and
    non-markdown files (e.g. PDFs). Returns '' if the folder is missing.
    """
    if not folder.is_dir():
        return ""
    files = sorted(folder.glob("*.md"))
    return "\n\n".join(f"## {f.name}\n{_read(f)}" for f in files)


def _write_output(filename: str, text: str) -> Path:
    """Write generated content to output/<filename> and return the path."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / filename
    out_path.write_text(text, encoding="utf-8")
    return out_path


def _generate(spec_path: Path, out_filename: str, tag: str, client: LLMClient) -> Path:
    """Shared generation routine: load spec + KB, call LLM, write output."""
    system, user = build_prompt_from_spec(
        spec=_read(spec_path),
        product_context=_load_folder(PRODUCT),
        primary_context=_load_folder(PRIMARY),
        secondary_context=_load_folder(SECONDARY),
    )
    result = client.generate(system, user)
    out_path = _write_output(out_filename, result.text)
    print(f"[{tag}] {out_filename} -> {out_path}  (via {result.provider} / {result.model})")
    return out_path


# ---------------------------------------------------------------------------
# One generator per Must
# ---------------------------------------------------------------------------
def generate_marketing_kit(client: LLMClient | None = None) -> Path:
    """Marketing promotion kit (Must M1)."""
    return _generate(SPEC_MARKETING, "marketing_kit.txt", "M1", client or LLMClient())


def generate_user_guide(client: LLMClient | None = None) -> Path:
    """Customer user guide (Must M2)."""
    return _generate(SPEC_USER_GUIDE, "user_guide.txt", "M2", client or LLMClient())


def generate_sales_one_pager(client: LLMClient | None = None) -> Path:
    """Sales one-pager (Must M3)."""
    return _generate(SPEC_SALES, "sales_one_pager.txt", "M3", client or LLMClient())


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main() -> None:
    """Run all three generators, reusing one client across outputs."""
    client = LLMClient()  # one client, shared → cheaper for the €5 budget
    generate_sales_one_pager(client)
    generate_marketing_kit(client)
    generate_user_guide(client)


if __name__ == "__main__":
    main()