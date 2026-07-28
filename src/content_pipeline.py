"""
content_pipeline.py — end-to-end generation pipeline (WBS 5.3).

Loads knowledge-base context + a markdown prompt spec, runs it through the LLM
client, and writes each output to output/.

Implemented: M1 (marketing kit), M2 (user guide), M3 (sales one-pager).
Run:  python -m src.content_pipeline      (from repo root)
"""

from __future__ import annotations

from pathlib import Path

try:
    from src.llm_integration import LLMClient
    from src.prompt_templates import build_prompt_from_spec
except ImportError:  # running as a sibling module (e.g. `from content_pipeline import ...`)
    from llm_integration import LLMClient
    from prompt_templates import build_prompt_from_spec

# ---------------------------------------------------------------------------
# PATHS — adjust these if your folder names differ. This is the only section
# you should need to touch.
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
KB = REPO_ROOT / "knowledge_base"
PRODUCT = KB / "product"        # PRD / release docs
PRIMARY = KB / "primary"        # company / brand / product info
SECONDARY = KB / "secondary"    # communication / tone / best practices

TEMPLATES = REPO_ROOT / "templates"   # prompt spec .md files live here
OUTPUT_DIR = REPO_ROOT / "output"

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


# ---------------------------------------------------------------------------
# Frontend seam — used by src/app_ui.py (Gradio UI).
# ---------------------------------------------------------------------------
SCOPES = ("all", "marketing", "customer_success", "sales")

_SCOPE_GENERATORS = {
    "marketing": [("email", generate_marketing_kit)],
    "customer_success": [("guide", generate_user_guide)],
    "sales": [("onepager", generate_sales_one_pager)],
}
_SCOPE_GENERATORS["all"] = (
    _SCOPE_GENERATORS["marketing"]
    + _SCOPE_GENERATORS["customer_success"]
    + _SCOPE_GENERATORS["sales"]
)


CURRENT_RELEASE = "Smart Home Configurator - Release v2.0.11"


def list_releases() -> list[str]:
    """Releases available to generate a kit for.

    The pipeline reads the whole knowledge_base/product/ folder as one
    feature's context (PRD, release notes, feature brief all describe the
    same release), per project_structure.md's single-feature POC scope — so
    this returns one label rather than one entry per file in that folder.
    """
    if not PRODUCT.is_dir() or not any(PRODUCT.glob("*.md")):
        return []
    return [CURRENT_RELEASE]


def generate_kit(feature_file: str, scope: str, temperature: float = 0.8) -> dict[str, str]:
    """Generate launch kit content for the current feature release.

    feature_file is accepted for forward-compatibility with a future
    multi-release KB, but today's pipeline reads the whole product/ folder
    per project_structure.md's single-feature POC scope, so it's unused for
    now beyond validating the caller's selection is one of list_releases().

    Args:
        feature_file: stem of a file in knowledge_base/product/ (see list_releases()).
        scope: one of SCOPES — "all", "marketing", "customer_success", "sales".
        temperature: LLM sampling temperature. Raise it for a "Regenerate" pass
            so a re-roll actually reads differently instead of nearly repeating.

    Returns:
        dict with a subset of keys {"email", "guide", "onepager"} depending on scope,
        each holding the generated text (read back from the file the backend wrote).
    """
    if scope not in SCOPES:
        raise ValueError(f"scope must be one of {SCOPES}, got {scope!r}")

    client = LLMClient(temperature=temperature)  # one client, shared across calls this run
    result = {}
    for key, generator in _SCOPE_GENERATORS[scope]:
        out_path = generator(client)
        result[key] = out_path.read_text(encoding="utf-8")
    return result