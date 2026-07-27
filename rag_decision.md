**Decision: non-RAG, static context injection.** Initially we are creating a proof of concept on a single feature to control for relevant output. Once we confirm that the feature launch kit works, we can then test it more broadly on different features. At this point, implementing RAG on the product feature release database would be a useful next step so the solution can replicate and scale across the organization's product development process. For the MVP, the pipeline loads every markdown file in a knowledge-base folder as-is and injects it directly into the prompt — no retrieval, no embeddings, no vector store.

*Corpus size & structure*
— The whole knowledge base (primary + secondary + product) is a handful of short markdown files, small enough to fit comfortably in a single prompt with room to spare. There is no volume that would force selective retrieval today.

*Change frequency*
— For the MVP the knowledge base is static: content only changes when a team member manually edits or adds a markdown file for a new release. There's no live or frequently-updating data source that would make static prompt-stuffing go stale between edits.

*Query diversity*
— The system doesn't field open-ended user questions against the knowledge base; it always runs one of three fixed prompt templates (marketing email, customer guide, sales one-pager) against the same small, known corpus. Retrieval is designed for picking a few relevant chunks out of a large, varied query space — with one predictable query shape and a corpus that already fits whole, there is nothing for retrieval to select down to.

*Context window, cost, and latency*
— The entire corpus is a few thousand tokens, well under any modern model's context limit, so stuffing it costs a small, predictable amount per generation (kept inside the project's €5 budget by defaulting to `gpt-4o-mini`). A retrieval step would add embedding cost, an index to maintain, and extra latency per call — overhead with no benefit at this corpus size.

*Complexity vs 2-day scope*
— A minimal loader (read every `.md` in a folder, concatenate, inject) plus three prompt templates was buildable and testable within the two-day window; a vector store and retrieval logic would not have been, and would not have improved output quality at this corpus size. Brand-aware uniqueness instead comes from the brand voice/persona files in the primary KB and the human-in-the-loop review step (edit and Pass/Fail before download), not from retrieval sophistication.

**Revisit when:** the knowledge base grows to cover multiple concurrent feature releases (not just one) or updates frequently enough that a person can no longer reasonably review the whole corpus before each generation — at that point, retrieving only the release-relevant subset of documents would keep prompts small and current.