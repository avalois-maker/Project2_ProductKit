---
source: https://feature-launch-kit.atlassian.net/wiki/spaces/~701210308bc81ff5e457699ca2ddbb9602f32/pages/557183
confluence_id: 557183
title: "PRD: Smart Home Configurator — Frontend Usability Improvements"
---

# Product Requirements Document

**Smart Home Configurator — Frontend Usability Improvements**

| Field | Value |
| --- | --- |
| Product | Smartivate Online Configurator (web) |
| Release | Frontend Change Set — September |
| Author | Anand Narasipuram |
| Status | Draft for development handover |
| Source | Configurator frontend change request (Sept), wireframe PPT |

## 1. Background

The Online Configurator guides users through a short question flow and returns a compatible, plug-and-play smart home product bundle matched to their preferences, budget and existing home infrastructure.

The current build deviates from the approved wireframes in several places. The gaps are concentrated in three areas: **navigation ergonomics**, **explanatory content visibility**, and **progress transparency**. Users cannot easily tell where they are in the flow, what a product category means, or which option they have selected.

## 2. Problem statement

Users drop out of the configurator because:

* Navigation controls sit far below the decision they are making, forcing a scroll-and-hunt loop.
* Explanatory text is hidden behind click or hover interactions that many users never discover.
* There is no visible sub-section progress, so the flow feels open-ended.
* Selection feedback is inconsistent between the configurator and the catalogue, so users are unsure whether their choice registered.

## 3. Goals

| Goal | Success measure |
| --- | --- |
| Reduce configurator abandonment | Completion rate of started configurator sessions |
| Reduce time-to-answer per question | Median seconds per question step |
| Increase comprehension of categories | Reduction in "Need Help?" chat opens per session |
| Restore wireframe parity | 100% of requirements below accepted in QA |

## 4. Scope

**In scope:** Frontend layout, interaction and copy changes to the configurator question flow and the configurator landing page.

**Out of scope:** Recommendation logic, product catalogue data model, pricing, checkout, backend APIs, mobile-native apps.

## 5. Requirements

### 5.1 Navigation

**REQ-NAV-01 — Reposition Prev / Next controls.** Move the Prev and Next buttons up to sit horizontally beside the answer images, left and right respectively, vertically centred against the image row.

* Buttons must remain visible without scrolling on standard desktop viewports (≥1280px wide).
* The existing bottom-of-page button positions are removed to avoid duplicate controls.
* Next stays disabled until a valid selection exists on required questions.

_Acceptance:_ On every question step, a user can advance or go back without scrolling below the image row.

### 5.2 Explanatory content

**REQ-HELP-01 — Always-visible question help text.** The text currently behind the ⓘ icon must be displayed permanently beneath the question headline. No click required.

* The ⓘ icon is either removed or retained purely as a visual marker.
* Applies to every question in the flow.

**REQ-HELP-02 — Restore missing option descriptions.** Each answer option must display its descriptive text, per the wireframes. Descriptions are currently missing in parts of the Efficiency, Security and Comfort sections.

* Descriptions render as static text below each option image (matching the treatment shown for Dimmer Switch / Control Switches / Buttons / Motion Sensors in the wireframes), not as hover-only tooltips.
* Text is truncated with consistent card height; full text remains readable without interaction.

**REQ-HELP-03 — Content audit.** Complete an inventory of all configurator options and confirm every one has: an image, a label, and a description. Missing product entries and missing copy must be filled before release.

_Acceptance:_ A checklist of all options exists, with zero items marked "missing image" or "missing text".

### 5.3 Selection feedback

**REQ-VIS-01 — Consistent selection highlight.** Apply the same shadow/elevation highlight used in the Catalogue section to selected option cards in the configurator.

* Hover state: subtle elevation.
* Selected state: persistent shadow plus the existing check-mark overlay.
* Identical CSS treatment across all questions, single-select and multi-select alike.

_Acceptance:_ Visual QA confirms configurator and catalogue card states are pixel-consistent.

### 5.4 Progress and wayfinding

**REQ-PROG-01 — Sub-section progress bar.** Introduce the chevron-style sub-section progress bar from the wireframes, showing the named steps within the current section.

* Example (Lighting section): Lighting → Heating
* Example (Security section): Cameras → Smart Door Locks → Door Bell → Window sensors → Smoke Detectors → Flood sensors → Burglar alarms

**REQ-PROG-02 — Apply across all sections.** The sub-section progress bar appears on every question in Efficiency, Security and Comfort, including all sub-sections. Step names and ordering follow the wireframe PPT.

**REQ-PROG-03 — Active step highlight.** The sub-section currently being answered is visually highlighted (distinct fill and text weight) versus completed and upcoming steps.

* Three visual states required: completed, active, upcoming.

**REQ-PROG-04 — Retain overall progress bar.** The existing percentage progress bar remains, positioned so that both the overall bar and the sub-section bar are visible simultaneously without conflict.

_Acceptance:_ On any question, a user can identify (a) which section they are in, (b) which sub-step is active, (c) how many sub-steps remain, and (d) overall completion percentage.

### 5.5 Configurator entry point

**REQ-ENTRY-01 — Configurator landing page.** Clicking CONFIGURATOR in the main navigation must open the configurator landing page containing the headline and introductory copy ("The Online Configurator for plug and play Smart Home devices!" plus the supporting paragraph), not the first question directly.

**REQ-ENTRY-02 — Start Configurator CTA.** The Start Configurator button on that landing page routes the user to the first configurator question.

_Acceptance:_ Navigation click → landing page with copy visible; CTA click → question 1.

## 6. Non-functional requirements

* **Responsive:** All changes hold at desktop, tablet and mobile breakpoints. Where the side-positioned Prev/Next (REQ-NAV-01) does not fit on narrow viewports, controls fall back to below the image row.
* **Consistency:** Reuse existing design tokens (colour, radius, shadow) from the catalogue components; no new one-off styles.
* **No regression:** "Start Over", "Need Help?" chat widget and the home icon continue to function unchanged.

## 7. Dependencies

* Wireframe PPT is the single source of truth for sub-section names, ordering and option copy.
* Catalogue component CSS must be available for reuse (REQ-VIS-01).
* Copy for missing option descriptions (REQ-HELP-02, REQ-HELP-03) to be supplied before development starts.

## 8. Prioritisation

| Priority | Requirements |
| --- | --- |
| P0 — blocks release | REQ-ENTRY-01, REQ-ENTRY-02, REQ-HELP-01, REQ-HELP-02, REQ-PROG-01, REQ-PROG-02, REQ-PROG-03 |
| P1 — high | REQ-NAV-01, REQ-VIS-01, REQ-HELP-03 |
| P2 — nice to have | REQ-PROG-04 layout refinement |

## 9. Open questions

1. Should the sub-section chevron bar be clickable for backward navigation, or display-only?
2. What is the exact fallback behaviour for Prev/Next on mobile — side controls, sticky footer, or swipe?
3. Are option descriptions final copy, or do they need a content review before implementation?
4. Which questions are mandatory versus skippable, so that the disabled state of Next can be defined precisely?
5. Does the overall percentage bar count sub-sections, or only top-level questions?
