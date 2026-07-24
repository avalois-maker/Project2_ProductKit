# Feature Launch Kit

Automation that turns feature release notes and documentation into launch enablement
materials: a marketing email (M1), a customer support/user guide (M2), and a sales
one-pager (M3).

Start with [`agents.md`](agents.md) for conventions and the repo map, and
[`project_structure.md`](project_structure.md) for scope, stakeholders and WBS.

## Layout

```
agents.md                                  project conventions for agents
project_structure.md                       Q/T/C, stakeholders, WBS, risks
knowledge_base/primary/
  feature_brief.md                         the PRD driving this launch
  brand_voice.md                           tone and messaging rules
  company_overview.md                      company/product facts
knowledge_base/secondary/
  launch_comms_best_practices.md           condensed external reference
templates/
  launch_communication_cascade.md          -> M1
  sales_enablement_kit.md                  -> M3
  rollout_strategy_planner.md              supporting
```

## Imported from Confluence

Source: `feature-launch-kit.atlassian.net`, personal space. Each file carries the
originating page ID and URL in its frontmatter.

Not yet imported: `document_processor.md` (page 426029) is empty in Confluence.
Still to create per `agents.md`: `sales_onepager_example.md`,
`marketing_email_example.md`, `support_guide_example.md`, `rag_decision.md`,
and everything under `src/`.
