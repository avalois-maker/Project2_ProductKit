# document\_processor\.md

## Purpose

This file tells a coding agent how to turn any raw source file into a clean markdown file ready for `knowledge_base/`. There is no parsing script — you do this extraction yourself, guided by these rules, whenever a new source document needs to go into the KB.

## When to use this

Any time a new source file shows up (in a folder, on Confluence, a link, or pasted content) and someone asks for it to be added to the knowledge base.

## Process

1. Read the full source, whatever the format — PDF, DOCX, PPTX, image, or URL. See "File-type notes" below for how to handle each.
2. Decide which KB it belongs in using the routing rules below. If it doesn't clearly fit one, ask before filing it.
3. Extract only the key facts relevant to that KB's purpose. Do not transcribe the source verbatim or dump the whole document in.
4. Write a new markdown file in the correct `knowledge_base/<primary|secondary|product>/` folder, snake\_case filename, one topic per file.
5. Do not add a header/metadata block (Source / Excluded / Last updated, etc.) — just the extracted facts as plain markdown.
6. Leave the original source file where it is for reference. Never delete it, and never treat it as itself part of the KB.

## Routing rules — which KB

- `knowledge_base/primary/` — general business info and company context: brand voice/tone, positioning, mission, company overview, general business facts
- `knowledge_base/secondary/` — research, best practices, industry standards, competitor info, "how others do it or say it" — used to evaluate the quality of outputs
- `knowledge_base/product/` — anything tied to a specific product or feature: release notes, PRDs, feature briefs, feature specs

## What to extract vs. exclude

Extract facts that would actually change what gets written in one of the three outputs (marketing email, support/user guide, sales one-pager): tone and voice rules, positioning, problem/solution framing, features and benefits, process steps, competitive differentiation, and any standards or best practices used to judge output quality.

Exclude anything that doesn't feed content generation: investor-only material (funding rounds, monetization/pricing model), personal bios and contact details, and anything outside the current single-feature POC scope.

## File-type notes

- **PDF** — extract the text; if a diagram or screenshot carries meaning (e.g. a process flow), describe it in words rather than referencing the image
- **DOCX / PPTX** — extract section or slide text the same way; briefly describe key visuals only if they carry information the text doesn't
- **Images** — describe what's visible and relevant in words; don't just link the image file
- **URLs** — fetch the page and extract the same way as a document

## Conventions

- Markdown only in `knowledge_base/` — no PDFs, images, or other formats stored there
- snake\_case filenames, one topic per file
- No standard header block on KB files — start directly with the extracted facts

## Never do

- Never copy the full raw source text into a KB file — always extract, never transcribe
- Never invent facts that aren't actually in the source
- Never file something in the wrong KB folder — check the routing rules first, ask if unclear
- Never delete or move the original source file
