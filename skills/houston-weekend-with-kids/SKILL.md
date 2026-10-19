---
name: houston-weekend-with-kids
description: Plan a Houston weekend with children through live searches for neighborhood activities, community events and major attractions, with a required weather check before itinerary and pass decisions. Use for local family discoveries, two-day plans and attraction-pass shopping.
license: MIT
compatibility: Requires file reading and current public-web research for checked plans. Optional source utility requires Python 3.14. No AI provider, model, account or separately installed shopping skill is required.
---

# Houston Weekend With Kids

Produce a practical two-day Houston plan from fresh local discovery and checked weather, then establish whether any admission pass helps. Search neighborhood places, community programs and changing events alongside major attractions. Match activities to the children's interests and admission categories, allow time for travel and breaks, and distinguish a provisional idea from a dated plan with verified entry requirements.

## Core Principles

- Choose experiences first. A pass's attraction count does not establish what fits the weekend or what the family wants.
- For open-ended planning, search beyond pass catalogs and the saved corpus. Local calendars, neighborhood organizations and resident-oriented sources discover candidates; organizers verify their current details. Preserve an explicitly fixed visit list or quote-review scope rather than adding unsolicited outings. Do not claim a place is known only to locals without evidence.
- Check current weather before choosing outdoor blocks or recommending weather-sensitive tickets. Return the forecast's coverage and the actual planning consequence; generic rain alternatives alone do not satisfy this check.
- Group each day around one or two nearby anchors. Check departure through return, including parking, walking, queues, meals and rest.
- Match visit depth to interests. Space Center Houston publishes short, half-day and full-day models; a tram or special tour changes the time needed.
- Keep unknown inputs visible. Two children establishes neither their admission categories nor the adult count.
- Treat published rules, estimated travel, observed availability and a completed reservation as separate facts. Recheck operational facts for the actual dates.
- Use public evidence for research. Protected values stay outside model context under `references/privacy-and-capabilities.md` and any stricter user/host policy; this bundle supplies no private-data adapter.

## Quick Command

From this skill's folder, run the following optional preview. It makes no network requests or writes and does not establish current hours or ticket availability. Before preparing input or using a result, read `schemas/command-rules.md` in full.

```sh
python -B scripts/public_sources.py --refresh --dry-run --json --no-input
```

## Context Requirements

This skill requires:

- Usable weekend windows, or explicit unknowns. Accept deliberately supplied planning dates/timing only when the caller's privacy policy permits model use. When their policy protects those values, keep them in local human-entry tools and use only qualified bounded fit results; otherwise keep affected plans conditional. Use Houston's `America/Chicago` timezone for timed plans/examples.
- Each child's venue-specific admission categories, child/adult counts, interests and priorities. Accept deliberate disclosure of permitted non-sensitive categories; names or birthdates are unnecessary for research.
- Attraction budget, pace and transport preference. A broad starting area may be used when deliberately supplied as non-sensitive; an exact home or lodging address is unnecessary for initial planning.
- Practical walking, rest, food or access preferences only through the caller's allowed boundary. Keep protected access/health records local; use qualified bounded fit results rather than retrieving protected records or requesting them in chat.
- Current official public rules for chosen attractions and pass restrictions returned by shopping. Missing inputs permit a clearly provisional result.

This skill produces:

- A freshly researched activity shortlist covering relevant local and non-pass options, and a realistic two-day outline or a bounded outline explaining open decisions.
- A pass-shopping handoff with desired admissions, feasible dates/slots and timing constraints, without duplicate price math.
- Official links with observation dates, a weather check with coverage/limits and effects on the plan, verified alternatives, required reservation actions and a clear status following `schemas/weekend-output.md`.

## Use Cases and Scenarios

### Route

Match the request to the most specific row and read its workflow before acting.

| User situation | Purpose | Workflow | Expected result |
|---|---|---|---|
| Only prices/deals/pass value are requested and intended visits are already fixed | Compare the fixed basket without expanding the visit list | read `playbooks/plan-houston-weekend.md`, section "Step 6: Hand feasible admissions to pass shopping" and read `schemas/weekend-output.md`, section "Pass-shopping handoff" | Current or explicitly conditional comparison for the desired visits |
| Dates, admission categories or preferences are missing | Offer useful choices and identify consequential gaps | read `playbooks/plan-houston-weekend.md` in full | Provisional alternatives and a short input request |
| Family wants local favorites, neighborhood activities or events beyond tourist lists | Discover current options suited to the family | read `playbooks/plan-houston-weekend.md` in full | Verified local candidates and weather-informed choices |
| Family wants Houston weekend attractions or passes | Establish trip fit and prepare shopping | read `playbooks/plan-houston-weekend.md` in full | Two-day outline and feasible admissions to price |
| A pass quote, trip date or forecast changes an outline | Reconcile changed constraints | read `playbooks/plan-houston-weekend.md` in full | Updated affected day and comparison assumptions |

## Scenario Workflows

### Procedure Sequence

The default path is one planning procedure with a shopping handoff when requested. Source maintenance is a supporting operation, not a prerequisite to every conversation.

| Stage / owner | Prerequisite and output | Receiving check | Next / return / stop |
|---|---|---|---|
| Frame / Step 1 | Request → known facts, unknowns and authority | Dates, categories and constraints are labeled honestly | Continue independent research; stop dependent precision when input is absent |
| Discovery / Step 2 | Interests and current public searches → local, event and attraction candidates, or an explicitly fixed visit list | Open-ended searches extend beyond the saved catalog; fixed scope is preserved and leads are distinguished from verified options | Step 3; broaden an open-ended search if only pass attractions were considered |
| Weather / Step 3 | Current official forecast/alerts → exposure and coverage assessment | Check time, location, valid periods, affected blocks and gaps are explicit | Step 4; missing evidence permits a conditional outline only |
| Evidence / Step 4 | Selected candidates → dated operational constraints | Organizer confirms occurrence, ages, admission, registration and closures | Step 5; return expired/unverified candidates to Step 2 |
| Fit / Step 5 | Verified candidates and weather → daily anchors and swaps | Dwell, movement, meals, rest and weather exposure fit | Step 6 for shopping, otherwise Step 7 |
| Shopping / Step 6 | Weather-adjusted desired admissions → comparison from shopping owner | Local/free choices, no-pass baseline, reduced use and flexibility remain in the comparison | Step 7; return cost/terms gaps to shopping, timing/weather gaps to Steps 3–5 |
| Reconcile / Step 7 | Draft and requested shopping result → checked recommendation | Discovery and weather evidence support choices; stale evidence is refreshed | Deliver and stop; no purchase/booking follows automatically |

Direct entry from a previously checked outline may reuse current inputs. Recheck changed dates, categories, rules, routes, pass terms or forecasts that invalidate acceptance. Planning-only work stops after the outline; source-maintenance-only work stops after its check. This sequence does not itself authorize delegation or external actions.

## Completion Criteria

- Open-ended planning considered suitable local/community activities outside the pass catalog, with organizer checks and an explanation of selection or exclusion. A saved attraction list is not sufficient; an intentionally fixed user-selected scope is identified and preserved.
- A current forecast/alert check records source, check time, area and valid periods, and explains its effect on each outdoor block and ticket flexibility. Missing dates, forecast coverage or retrieval remain explicit; no checked dated plan is claimed without that evidence.
- Daily anchors, visit depth, travel/arrival, food/rest and weather/capacity alternatives fit stated available windows.
- Actual dates, hours/last entry, admission categories, reservations and relevant pass terms are checked where necessary; unknowns remain visible.
- Shopping covers only desired feasible visits. Expiry/activation covers the schedule or the mismatch is disclosed.
- The result states what is proposed, checked and still awaiting input, reservation or purchase authority.
- Missing dates/categories produce a provisional recommendation without final household totals or confirmed capacity claims.
- A dated plan may use deliberately supplied policy-permitted dates and current public evidence. If essential dates or other values are protected by the caller's policy, require qualified fit results or keep affected claims conditional. Unchecked live capacity remains explicitly unverified under either path.

## Supporting Resources

- Before planning, read `playbooks/plan-houston-weekend.md` in full.
- Before choosing anchors or resolving venue constraints, read `references/houston-planning.md` in full.
- Before live discovery or the weather check, read `references/local-discovery-and-weather.md` in full. The fixed source collector supplies background only; live search and forecast retrieval use the host's available public-web tools.
- Before returning an outline or shopping handoff, read `schemas/weekend-output.md` in full.
- Before source commands, read `schemas/command-rules.md` in full. `scripts/README.md` supplies tool quick start; `assets/source-catalog.json` owns reviewed source IDs.
- Before gathering inputs or selecting host tools, read `references/privacy-and-capabilities.md` in full. It owns private-data boundaries and the optional shopping integration contract.
- When exact source wording matters, open the official source linked in `references/houston-planning.md`. If a locally generated corpus exists, its `corpus/inventory.json` maps source files and timestamps. Preserve origin, observation date and representation limits; saved HTML is not live capacity. The public package does not distribute full third-party source copies.
- For maintenance and future checks, read `skill-ci/README.md` in full. No documentation database or external workspace is required to use this package.

## Critical Constraints

- Planning/research do not authorize purchases, bookings, messages, account changes or reservation submission. Apply explicit action authority already supplied in the session.
- Do not inspect protected records, accounts, filled pages, screenshots or secrets for public planning. Request protected missing input through an actually supported local entry tool; never solicit it in chat or invent an adapter.
- Apply the caller's actual privacy policy before using dates/timing, origin, lodging or access needs. Accept deliberately supplied planning inputs only when that policy permits; protected values stay outside model context and tool/search outputs. Missing required private-fit tooling limits affected claims, not ordinary permitted-date planning.
- Browser work follows the user's applicable session policy and `references/privacy-and-capabilities.md`. Preserve existing sessions; do not launch, restart or replace them without authority. The public-source CLI uses fixed public HTTP GETs without browser/cookies.
- Do not claim inclusion of tram add-ons, special exhibits, rides, parking or reservations without current appropriate terms. Shopping owns price/product claims.
- Do not store sensitive family details or task histories in this bundle/corpus or turn tentative trip facts into lasting preferences.
- Keep reusable instructions/tools in Git and generated third-party source copies local/ignored. Keep private task histories outside this package. Model trials require an explicit request.

## Recovery States

- **Completed:** The requested planning or planning-and-shopping result is checked to its stated scope and next actions are clear.
- **Completed with gaps:** A useful provisional outline has explicit missing dates/categories, route or availability; dependent precision is withheld.
- **Blocked:** An essential source, private adapter, preference or authority prevents the requested dependent result. Explain the exact gap and preserve independent accepted work.
