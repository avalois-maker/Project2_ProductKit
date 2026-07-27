# Feature Launch Kit

Turns a feature's release notes/PRD into launch enablement materials, grounded in the
product's knowledge base: a marketing email (M1), a customer support/user guide (M2),
and a sales one-pager (M3). Two LLM providers are wired in (OpenAI primary, Cohere
fallback) so a single provider outage doesn't stop generation.

Start with [`agent md files/agents.md`](agent%20md%20files/agents.md) for conventions
and the repo map, and [`project_structure.md`](project_structure.md) for scope,
stakeholders, and the WBS.

## Run it

**One-click (recommended):** double-click `Launch Web App_Windows.bat` (Windows) or
`Launch Web App_Mac-Linux.command` (Mac/Linux). First run creates a `.venv`, installs
`requirements.txt`, and copies `.env.example` to `.env` — fill in your API keys there,
then re-run. Subsequent runs just launch the Gradio app in your browser.

**Manual:**
```
pip install -r requirements.txt
cp .env.example .env   # add OPENAI_API_KEY / COHERE_API_KEY
cd src && python app_ui.py
```

**CLI only** (skips the UI, runs all three generators, writes to `output/`):
```
python -m src.content_pipeline
```

**Tests:** `pytest` (from repo root).

## Layout

```
agent md files/
  agents.md                                agent conventions + repo map (read first)
  document_processor.md                    how to extract a raw source doc into the KB
project_structure.md                       Q/T/C, stakeholders, Must-haves, WBS, risks
rag_decision.md                             why no RAG for this POC (single-feature scope)

knowledge_base/
  primary/                                 brand voice, company overview, persona,
                                            past_content/ (empty, reserved)
  secondary/                               launch comms best practices, rollout planner,
                                            sales enablement kit — used to judge output quality
  product/                                 the active release: PRD, release notes, feature brief

templates/
  marketing_email.md                       prompt spec -> M1
  customer_guide.md                        prompt spec -> M2
  sales_onepager.md                        prompt spec -> M3

src/
  app_ui.py                                Gradio frontend (select -> generating -> review -> download)
  content_pipeline.py                      loads KB + template, calls the LLM, writes output/
  llm_integration.py                       LLMClient — OpenAI primary, Cohere fallback
  prompt_templates.py                      builds (system, user) prompts from a template spec
  render_template.qmd, quarto_style.css    Quarto template for the downloadable styled HTML kit

tests/
  test_content_pipeline.py                 KB loading, scope validation, generator mapping
  test_app_ui.py                           pure helpers in app_ui.py (HTML/update builders)

output/                                    generated kit files (gitignored)
assets/logo_smartivate.png                 UI logo
Day1_kanban.png                            board screenshot (WBS 6.3)
Smart_Home_Configurator_Communications_Pack.html   sample rendered output for the current release
prompt.txt                                 original agent bootstrap prompt used to scope this build
requirements.txt, .env.example             dependencies and config template
```

## Imported from Confluence

Source: `feature-launch-kit.atlassian.net`, personal space. Files carrying that
provenance note it in frontmatter.
