"""
prompt_templates.py — prompt engineering templates (WBS 5.2).

One generic builder for all three outputs. The instruction/role text lives in
a markdown spec file (e.g. templates/marketing.md); this module loads the
knowledge-base content and injects it, since an LLM over an API cannot read
local files itself. This is our non-RAG context-injection approach.
"""

from __future__ import annotations


def build_prompt_from_spec(
    spec: str,
    product_context: str,
    primary_context: str = "",
    secondary_context: str = "",
) -> tuple[str, str]:
    """
    Build (system, user) from a markdown prompt spec + injected KB context.

    spec              — role/instruction markdown (e.g. marketing.md). Becomes
                        the system prompt.
    product_context   — the PRD / release doc(s)  (knowledge_base/product/).
    primary_context   — company / brand / product info (knowledge_base/primary/).
    secondary_context — communication / tone / best practices (secondary/).
    """
    system = spec.strip()

    parts = [
        "The files referenced in your instructions are provided inline below. "
        "Use ONLY this content as your source of truth. Do not invent features, "
        "metrics, pricing, or benefits that are not present in this content.\n"
    ]
    parts.append(f"=== PRODUCT / RELEASE DOCUMENT ===\n{product_context.strip()}")

    if primary_context.strip():
        parts.append(
            f"=== COMPANY / BRAND / PRODUCT CONTEXT ===\n{primary_context.strip()}"
        )
    if secondary_context.strip():
        parts.append(
            f"=== COMMUNICATION / TONE / BEST PRACTICES ===\n{secondary_context.strip()}"
        )

    user = "\n\n".join(parts)
    return system, user