"""
prompt_templates.py — advanced prompt templates (WBS 5.2).

Sales One-Pager: core value messaging for the sales team.
Maps to Must M3 in project_structure.md.
"""

# Voice + anti-"AI-slop" guardrails live in the SYSTEM prompt so every
# template shares the same brand discipline (Hivemind strategy: unique POV).
SALES_ONE_PAGER_SYSTEM = """You are a senior product marketing manager writing \
an internal sales enablement one-pager. Your reader is a salesperson who has \
90 seconds before a customer call and needs the core value messaging for a \
newly released feature.

Write in this brand voice:
{brand_voice}

Hard rules:
- Lead with the customer's problem and the outcome, never the feature name.
- Every claim must trace to the provided feature or research context. Do NOT \
invent numbers, integrations, or capabilities.
- No generic filler ("in today's fast-paced world", "game-changer", \
"revolutionary", "unlock", "seamless"). If a sentence could describe any \
product, delete it.
- Concrete over abstract: name the specific job the feature does.

Output EXACTLY these sections as plain text (no markdown headers heavier than \
a line label):

FEATURE: <name>
THE PROBLEM IT SOLVES: <2 sentences, customer's words>
CORE VALUE MESSAGE: <one sharp sentence sales can repeat verbatim>
TOP 3 TALKING POINTS:
  1. <benefit — why the customer cares, not what it does>
  2. ...
  3. ...
OBJECTION HANDLING:
  - "<likely objection>" -> <one-line rebuttal grounded in context>
  - "<likely objection>" -> <rebuttal>
IDEAL CUSTOMER: <who feels this pain most>
"""


def build_sales_one_pager_prompt(
    feature_context: str,
    brand_context: str,
    research_context: str = "",
) -> tuple[str, str]:
    """
    Build (system, user) prompts for the sales one-pager.

    feature_context  — Primary KB: what the feature is/does (markdown text).
    brand_context    — Primary KB: brand voice / messaging guidelines.
    research_context — Secondary KB: market/competitor notes (optional).

    Returns (system_prompt, user_prompt) ready for LLMClient.generate().
    """
    system = SALES_ONE_PAGER_SYSTEM.format(brand_voice=brand_context.strip())

    research_block = (
        f"\n\nMARKET / COMPETITOR CONTEXT (use to sharpen positioning, "
        f"do not quote verbatim):\n{research_context.strip()}"
        if research_context.strip()
        else ""
    )

    user = (
        "Write the sales one-pager using ONLY the context below.\n\n"
        f"FEATURE CONTEXT (primary source of truth):\n{feature_context.strip()}"
        f"{research_block}"
    )
    return system, user