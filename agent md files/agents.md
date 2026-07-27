# agents\.md

### Purpose

You are working in the [https://github.com/avalois-maker/Project2\_ProductKit](https://github.com/avalois-maker/Project2_ProductKit) repo. It turns a feature/release note into three outputs — a marketing email, a customer support/user guide, and a sales one-pager — for Sales, Customer Relations, and Marketing. Before writing code, check `project_structure.md` for the Must haves table and confirm which Must ID the active card maps to. Every change you make should be traceable to one of the mush have IDs — if it isn't, stop and ask rather than building it.

### Stack & run

- Python 3.8+
- UI (recommended): double-click `Launch Web App_Windows.bat` / `Launch Web App_Mac-Linux.command`, or `cd src && python app_ui.py` — opens the Gradio app in your browser.
- CLI only (skips the UI, runs all three generators, writes to `output/`): `python -m src.content_pipeline`
- Two LLM providers in use ("two brains") — API keys in `.env` (copy from `.env.example`), never hardcoded, never printed, never committed:
    - `OPENAI_API_KEY`
    - `COHERE_API_KEY`

### Repo map — put new files here, not elsewhere

- `knowledge_base/primary/ — general business info and company context: brand voice/tone, positioning, mission, company overview, general business facts`
- `knowledge_base/secondary/ — research, best practices, industry standards, competitor info, "how others do it or say it" — used to evaluate the quality of outputs`
- `knowledge_base/product/ — anything tied to a specific product or feature: release notes, PRDs, feature briefs, feature specs`
- `templates/` — one prompt template per output (email, guide, one-pager); this defines the shape of each output — edit templates here, not inline in pipeline code
- `src/content_pipeline.py` — loads KB + a template spec, calls the LLM, writes `output/`; also exposes `generate_kit()`/`list_releases()` for the UI
- `src/prompt_templates.py` — builds the (system, user) prompt from a template spec + KB context
- `src/llm_integration.py` — LLM API wrapper (`LLMClient`, wraps both providers)
- `src/app_ui.py` — Gradio frontend (Select → Generating → Review → Download)
- `src/render_template.qmd`, `src/quarto_style.css` — Quarto template for the downloadable styled HTML/Markdown kit
- `rag_decision.md`, `project_structure.md` — read these before building anything KB- or RAG-related

### Conventions — follow these without being asked

- KB content is markdown only, one topic per file, in the correct folder (primary / secondary / product) — never mix folders
- Do not write a document-parsing script. Load markdown as-is and pass it to the LLM; the instructions for how to use each KB live here and in `templates/`, not in custom parsing code
- If adding a new source doc, extract key facts into a short markdown file first (see how brand guidelines/pitch deck were handled) — don't dump full source PDFs into the KB
- `llm_integration.py` wraps both providers — check the docstring/comments there (or `rag_decision.md` if the split is RAG-related) before assuming which model handles which step; don't default to one provider for everything
- snake\_case filenames

### Definition of Done — a change isn't done until:

- It matches the Kanban DoD
- It touches only the active card's Must ID — nothing else
- No secrets are committed

### Never do — even if it seems helpful

- Never commit `.env` or any API key
- Never expand scope into the Won't list without the team agreeing first
- Never invent an API, a KB fact, or a product detail that isn't actually in `knowledge_base/`
- Never add multi-feature batching, extra output formats, or anything not in the Must table — ask first

### How you'll be used

- This file is your first read, every session — if instructions here conflict with something else, this file wins.
- If you notice yourself drifting off-scope mid-task, stop and re-read this file plus the active card's Must ID before continuing.
