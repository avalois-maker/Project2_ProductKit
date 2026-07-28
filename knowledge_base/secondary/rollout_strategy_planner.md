---
source: https://feature-launch-kit.atlassian.net/wiki/spaces/~701210308bc81ff5e457699ca2ddbb9602f32/pages/360497
confluence_id: 360497
title: "Rollout strategy — condensed industry notes"
note: >
  Condensed notes extracted from the original prompt-template draft on this
  Confluence page. The full draft (role instructions, fill-in-the-blank
  template) is not reproduced here — it belongs in templates/, not the
  knowledge base, since KB content should inform how a launch is framed,
  not dictate a competing output structure for the LLM to follow.
---

# Rollout strategy — secondary KB

Industry practice for how software features move from build to full release,
useful context when framing how confidently a launch communication should
describe a feature's rollout stage:

- **Risk determines rollout speed.** Low-risk changes (UI-only, optional,
  small user base) can launch broadly right away. Higher-risk changes
  (backend/data changes, auth or billing, irreversible operations) typically
  roll out in phases: internal-only, then a small canary group, then
  expanding to more users, then full launch.
- **Each phase has a purpose**, not just a percentage: internal testing
  catches obvious bugs; a canary release catches production-specific issues
  at small scale; broader phases build confidence before committing to
  everyone.
- **A rollout can pause or roll back at any phase** if a metric degrades,
  an incident occurs, or something can't be explained — that's expected
  discipline, not a sign the feature failed.
- **The cost of a bad incident usually outweighs the cost of a slower
  rollout.** A well-designed rollout is built to catch problems while
  they're still small and reversible.

For launch communications, this means: avoid language that implies a launch
is finished, permanent, or fully rolled out to everyone unless the actual
release notes/PRD confirm that's the case for this feature.
