# Release Notes — Smartivate Configurator

**Product:** Smartivate Online Configurator
**Release:** v1.4.0
**Date:** [release date]
**Audience:** End users (public notes) + internal stakeholders (traceability section)

> **Before publishing:** items below are written from the approved PRD, not from a verified build. Confirm each one actually shipped and delete anything that slipped to the next release.

---

## In this release

The configurator now tells you where you are, what each option means, and what happens next. You no longer have to hover, click or scroll to find that out.

---

## New

### Configurator start page
Selecting **Configurator** in the main menu now opens a short introduction explaining what the tool does before any questions begin. **Start Configurator** takes you into the first question when you're ready.

*Why it matters:* people arriving from the menu previously landed mid-flow with no explanation of what they had started.

### Step-by-step progress within each section
Every section — Efficiency, Security and Comfort — now shows its own sequence of steps above the question. In Security, for example, you can see the full path from Cameras through Smart Door Locks, Door Bell, Window sensors, Smoke Detectors, Flood sensors and Burglar alarms.

The step you are answering is highlighted, so completed, current and upcoming steps are distinguishable at a glance.

*Why it matters:* the flow now has a visible end, which is the single largest driver of drop-out in question-based tools.

---

## Improved

### Help text is always visible
Explanations previously hidden behind the ⓘ icon are now shown permanently beneath each question. Nothing to click.

### Option descriptions restored across all questions
Each option — dimmer switches, control switches, motion sensors, indoor and outdoor cameras and the rest — now carries its description as static text on the card rather than as a hover tooltip.

*Why it matters:* hover text is invisible on touch devices and undiscoverable for most desktop users, so a large share of the explanatory content was never being read.

### Navigation moved next to your choices
**Prev** and **Next** now sit either side of the option images instead of below the fold. You can move through the flow without scrolling.

### Consistent selection feedback
Selecting an option applies the same shadow and highlight used in the catalogue, plus a check overlay. Selection behaves identically in both parts of the site.

---

## Fixed

- Missing option images and descriptions have been audited and completed across all questions.
- The overall percentage progress bar has been repositioned so it no longer conflicts with the new section progress bar; both are visible at once.
- Duplicate navigation controls at the foot of the question page have been removed.

---

## Known limitations

- On narrow viewports, **Prev** and **Next** fall back to below the option row rather than beside it.
- The section progress bar is display-only; you cannot yet click a completed step to jump back to it.
- Option descriptions are truncated to a fixed card height on questions with many options.

---

## Traceability

| Release item | PRD requirement | Priority |
|---|---|---|
| Configurator start page | REQ-ENTRY-01, REQ-ENTRY-02 | P0 |
| Section progress bar | REQ-PROG-01, REQ-PROG-02 | P0 |
| Active step highlight | REQ-PROG-03 | P0 |
| Always-visible help text | REQ-HELP-01 | P0 |
| Option descriptions | REQ-HELP-02 | P0 |
| Content audit | REQ-HELP-03 | P1 |
| Navigation repositioned | REQ-NAV-01 | P1 |
| Selection highlight | REQ-VIS-01 | P1 |
| Progress bar layout | REQ-PROG-04 | P2 |

---
---

# Template — for reuse on future releases

Copy the structure below. Two rules make release notes usable rather than decorative:

1. **Lead with the user outcome, not the ticket.** "Step-by-step progress within each section" beats "Implemented REQ-PROG-01". Keep requirement IDs in the traceability table where auditors need them, out of the prose where users don't.
2. **Publish known limitations.** Support volume drops when people can see that a gap is known rather than assuming they've done something wrong.

```markdown
# Release Notes — [Product]

**Release:** [version]
**Date:** [date]
**Audience:** [who this is written for]

## In this release
[Two or three sentences. What is materially different for the user now.]

## New
### [Feature name in user language]
[What it does, in plain terms.]
*Why it matters:* [the problem it removes]

## Improved
### [Change name]
[What changed and what the user will notice.]

## Fixed
- [Defect resolved, described by symptom rather than cause]

## Known limitations
- [Gap that is known and accepted for this release]

## Traceability
| Release item | Requirement | Priority |
|---|---|---|
| | | |
```

**Versioning convention:** MAJOR.MINOR.PATCH — MAJOR for breaking changes to a user's saved configuration, MINOR for new user-facing capability, PATCH for fixes only.

**Tone:** matches the brand voice reference — reassuring rather than technical, warm and second-person, concrete about what changed. Notes are published in EN and DE; both must read as native, not translated.
