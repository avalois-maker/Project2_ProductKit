---
source: https://feature-launch-kit.atlassian.net/wiki/spaces/~701210308bc81ff5e457699ca2ddbb9602f32/pages/950310
confluence_id: 950310
---

## Purpose

This repo builds an automation that turns feature release notes and documentation into a feature launch kit. The goal is to provide relevant teams with enablement materials to communicate effectively the feature launch in their workstream. For this project it is scoped to a marketing email, a customer support/user guide, and a sales one-pager. This way, Sales, Customer Relations, and Marketing can each start their workstream in week 1 of a feature launch. See `project_structure.md` for the full Q/T/C, stakeholders, and WBS. Must IDs M1–M3 (below) map directly to the three outputs; work should always be traceable back to one of them.

## Stack & run

* Python 3.8+
* Main command: `python src/main.py --feature knowledge_base/primary/feature_brief.md` _(confirm exact CLI name/args once main.py is finalized)_
* Env vars (set in `.env`, never commit it):
    * `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` — whichever LLM provider was chosen
    * _(add any others once llm_integration.py is built)_

## Repo map

* `knowledge_base/primary/` — company/feature-specific source material: `feature_brief.md`, `sales_onepager_example.md`, `marketing_email_example.md`, `support_guide_example.md`, `brand_voice.md`, `company_overview.md`
* `knowledge_base/secondary/` — external context: `launch_comms_best_practices.md`
* `src/document_processor.py` — markdown ingestion for both KBs
* `src/knowledge_base.py` — primary/secondary KB loader/selector
* `src/prompt_templates.py` — the three output templates (email, guide, one-pager)
* `src/llm_integration.py` — LLM API wrapper
* `src/content_pipeline.py`, `src/main.py` — end-to-end pipeline entry point
* `rag_decision.md`, `project_structure.md` — PM/RAG docs at repo root

## Conventions

* All KB content is markdown, one topic per file, saved under the correct `primary/` or `secondary/` folder — never mixed.
* New source files go through the hybrid process already used for the brand guidelines and pitch deck: key facts extracted into a short markdown file, full source kept in Confluence/Data folder for reference only.
* Snake_case filenames; one prompt template per output type in `prompt_templates.py`.

## Definition of Done (agent changes)

* Matches Kanban DoD
* Touches only the active card / Must ID
* No secrets committed

## Never do

* Commit `.env` or API keys
* Expand into the Won't list without team agreement
* Invent APIs or KB facts — pull only from what's actually in `knowledge_base/`

## How we use agents

* One Kanban card at a time; paste card title + Must ID into the agent prompt
* Point the agent at this file first
