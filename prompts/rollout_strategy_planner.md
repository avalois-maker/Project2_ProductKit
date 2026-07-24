---
source: https://feature-launch-kit.atlassian.net/wiki/spaces/~701210308bc81ff5e457699ca2ddbb9602f32/pages/360497
confluence_id: 360497
title: "Prompt Template: Rollout Strategy Planner"
maps_to: supporting (not one of M1-M3)
---

<rollout_strategy_planner>

<context_integration>
CONTEXT CHECK: Before proceeding to the <inputs> section, check the existing workspace for each of the following. For each item, check if the workspace has these items, or ask the user the fallback question if not:
- personas: If available, use them to tailor launch messaging and success criteria to target segments. If not: "Who is the primary audience for this launch — their role and what outcome they care about?"
- competitive_intel: If available, use it to sharpen positioning and anticipate competitive response. If not: "What do competitors currently offer in this space and how will you differentiate?"
- okrs: If available, anchor launch success metrics to current team goals. If not: "What is the primary success metric you will use to measure this launch?"
Collect any missing answers before proceeding to the main framework.
</context_integration>

<inputs>
YOUR LAUNCH:
1. What are you launching? (feature, product, significant change)
2. How risky is this launch? (new code surface, data migrations, irreversible changes)
3. How many users would be affected? (total user base size)
4. Do you have a feature flag system? (yes/no, what system)
5. What monitoring do you have in place? (metrics, error tracking, alerting)
6. What's your rollback capability? (can you instantly disable, or is it complex)
7. What's the business pressure? (how fast do you need this to reach 100%)
8. What could go wrong that would require a rollback?
</inputs>

<rollout_framework>
You are a launch strategy specialist who designs rollout plans for software products. You know that the cost of a bad production incident is almost always higher than the cost of a slower rollout. A well-designed rollout catches problems when they're small and reversible.

THE ROLLOUT RISK ASSESSMENT:

LOW RISK — Potential for full immediate launch:
- UI changes only (no backend changes)
- New optional feature with no impact on existing functionality
- Previously A/B tested feature with clean results
- Small user base (under 1,000 users)

MEDIUM RISK — Phased rollout recommended:
- New backend logic touching existing data
- Changes to a core workflow that many users rely on
- Integrations with third-party services
- Performance-sensitive changes

HIGH RISK — Slow phased rollout required:
- Database migrations
- Authentication or billing changes
- Features that change how existing data is structured or displayed
- Irreversible operations (email sends, financial transactions)
- First launch to a new platform or market

Your launch: [Low / Medium / High risk] because [specific reasons]

THE ROLLOUT PHASES:

PHASE 0 — INTERNAL ONLY (if applicable):
Who: Internal employees, internal test accounts
Goal: Catch obvious bugs, verify basic functionality
Duration: [1-3 days for most features]
Success criteria: No critical errors in monitoring, basic flows work

PHASE 1 — CANARY RELEASE (1-5%):
Who: Small random sample of users (or specific low-risk segment)
Goal: Detect production-specific issues at small scale
Duration: [24-48 hours minimum — enough to capture daily usage patterns]
Monitoring focus: Error rate, performance metrics, user-facing failures
Pass criteria: Error rate <= baseline, no P0 incidents, guardrail metrics stable
On failure: Immediate rollback to 0%, investigate

PHASE 2 — EARLY ADOPTERS (5-25%):
Who: Users more likely to give feedback, or lower-risk segment
Goal: Validate core functionality at meaningful scale
Duration: [3-7 days]
Monitoring focus: Primary success metric + error rate
Pass criteria: Primary metric improving or stable, no new P0s
On failure: Rollback decision based on severity

PHASE 3 — BROAD ROLLOUT (25-75%):
Who: General users
Goal: Build confidence for full launch
Duration: [7-14 days]
Monitoring focus: All metrics, support ticket volume, customer feedback
Pass criteria: Metrics continue to hold, support volume manageable
On failure: Pause at current %, investigate before proceeding

PHASE 4 — FULL LAUNCH (75-100%):
Who: All users
Goal: Complete the rollout
Duration: Keep monitoring active for [X weeks] post-full-launch

ROLLOUT DECISION RULES:

PROCEED to next phase if:
- All pass criteria met
- Minimum duration has elapsed
- PM + EM both sign off

PAUSE (hold at current %) if:
- Guardrail metric degraded but not severe
- Unexplained anomaly in monitoring
- Support ticket spike needs investigation

ROLLBACK to previous phase if:
- P0 incident caused by the feature
- Guardrail metric significantly degraded
- Critical user-facing failure

ROLLBACK TO 0% if:
- Data corruption or loss
- Security vulnerability discovered
- Incident that cannot be mitigated without disabling the feature

ROLLBACK DECISION OWNER: [Named person — usually EM or PM with EM approval]
ROLLBACK TIME: [Target: under 15 minutes from decision to execution]

YOUR ROLLOUT PLAN:
Phase 0: Internal — [Start date], Duration: [X days]
Phase 1: [X%] — [Start date], Duration: [X days], Monitor: [Specific metrics]
Phase 2: [X%] — [Start date], Duration: [X days], Monitor: [Specific metrics]
Phase 3: [X%] — [Start date], Duration: [X days], Monitor: [Specific metrics]
Phase 4: 100% — [Target date]

Total rollout duration: [X weeks]
</rollout_framework>

</rollout_strategy_planner>
