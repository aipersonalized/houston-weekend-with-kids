# Weekend Planning Output Contract

This human-readable contract owns fields shared by Houston planning and pass shopping. It is not an executable validator or private-data schema. Include necessary fields only; mark unavailable inputs unknown.

## Trip result

- **Status:** Provisional outline, checked dated plan or blocked dependent result; say what was established.
- **Discovery evidence:** Local/community and other candidates considered, discovery and organizer links, occurrence/age/access checks, and reasons for selection or exclusion. Show that the search extended beyond saved tourist/pass lists, or state an intentionally narrow user-selected scope.
- **Weather assessment:** Official forecast/alert links, checked time/timezone, issue time when available, area and valid periods, relevant conditions/alerts, and effects on exposed visits, travel and ticket flexibility. State unmatched dates, coverage limits or failed retrieval; generic contingencies alone are insufficient.
- **Known requirements/gaps:** Policy-permitted deliberately supplied dates, anonymous admission categories, child/adult counts, allowed window-fit statuses, priorities, budget/pace and transport. Exclude values protected by the caller's policy, names, birthdates, exact addresses, account/booking identifiers, private communications and private health records. For protected dates use only bounded fit/status results.
- **Daily outline:** Day 1/Day 2, permitted actual or explicitly illustrative time windows in Houston's timezone, anchors, visit depth/duration and basis; movement/arrival, meals/rest, a verified swap with its weather/capacity trigger, and entry/boarding cutoffs. When necessary dates/routes are protected, matching stays in qualified local adapters; missing required fit evidence keeps affected claims conditional. Ordinary permitted-date planning needs no such adapter. Label unverified live capacity.
- **Admission dependencies:** Required ticket, timed reservation, show/tour/add-on, lead time and check state. Separate general entry from special access.
- **Recommendation:** Explain fit to interests/time; use the shopping owner's comparison when requested.
- **Evidence:** Official links, observation dates and material limits. Label estimates/unavailable live checks.
- **Next action:** Smallest consequential input or reservation action; distinguish proposed, checked, reserved and purchased.

## Pass-shopping handoff

Producer: Houston planning. Receiver: The current agent's comparison role, or an optional installed shopping skill whose actual contract has been checked. Permitted effects: public comparison under current authority without an implied purchase, booking, message or account action. No external skill is required; read `references/privacy-and-capabilities.md`, section "Optional shopping integration" for fallback ownership.

| Field | Required meaning |
|---|---|
| Trip window | Deliberately supplied dates permitted by the caller's policy; when dates are protected, use an opaque local reference or qualified bounded fit status under an existing supported contract; otherwise unknown |
| Party | Known adult count and each child's admission categories; preserve unknowns/protected-value boundaries |
| Desired activities and admissions | Full prioritized basket, including local/free/non-pass choices and essential add-ons; mark swaps so shopping does not count both or invent extra savings |
| Weather and reduced use | Allowed weather assessment/status, exposed visits, verified substitutes, possible removed paid visits and flexibility needs; no raw private dates |
| Feasible slots | Proposed day/time windows and dwell; capacity unverified, publicly observed or separately reserved |
| Constraints | Relevant transport, pace, breaks and entry dependencies using allowed non-sensitive task results |
| Budget | User-supplied amount/currency and scope, or unknown |
| Evidence | Official links/observation dates and unresolved conflicts |
| Requested return | Current costed options for the same set; category mapping; inclusion/exclusion; validity/expiry/activation; reservations/capacity; fees/returns; unknowns |

Shopping checks the handoff before pricing, retains a no-pass baseline and reprices when weather or local alternatives change paid use. Planning accepts products only when terms/dates/weather fit intended visits. Return price/terms defects to shopping and route/timing/weather defects to planning. Stop after the requested result; no external action follows automatically.
