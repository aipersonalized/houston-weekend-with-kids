# Privacy and Capability Contract

### When to Load

Read in full before collecting trip inputs, using browser tools or requesting a private-data operation. This is the portable baseline; apply stricter user or host policy when present.

### Quick Reference

Use public research and minimal anonymous preferences. Keep protected family values outside model context. Check what the host's tools actually support; an instruction file supplies no isolation or private-data adapter.

## Detailed Content

### Inputs

Planning dates/timing, anonymous venue admission bands, child/adult counts, interests, budget and pace may be deliberately supplied when the caller's privacy policy permits model use. Deliberate disclosure does not override an existing policy that forbids those values in model context. Do not request names, birthdates, booking/account identifiers or exact addresses for public research.

Values protected by the caller's actual policy stay outside prompts, search queries, screenshots, logs and agent-visible tool results. These may include upcoming dates/timing, origin, lodging and access needs; credentials and private health/account records remain protected. Use a supported local human-entry tool and a qualified adapter that resolves such values locally and returns only purpose-limited fit/status results. Do not invent that capability or solicit values forbidden in chat. Continue with provisional public alternatives when required protected-fit evidence is unavailable. Ordinary hosts can produce a dated plan from policy-permitted deliberately supplied dates without a private-date adapter.

### Required and optional capabilities

| Capability | Use and missing-capability behavior |
|---|---|
| Read bundled Markdown/resources | Required to follow the complete workflow; report inaccessible resources |
| Current public-web search and page retrieval | Needed for live discovery, organizer rules and official forecasts/alerts; unavailable evidence keeps results provisional |
| Local private human entry and bounded fit adapter | Needed only when required inputs are protected by the caller's policy. Its absence limits affected protected-fit claims; permitted-date public planning can proceed |
| Pass comparison | Can be performed by this agent using public official terms, or by an optional installed shopping skill after checking its contract |
| Python 3.14 | Optional fixed-source utility only; no effect on the ability to follow the planning instructions |

Public-web tools must not attach account cookies or expose signed-in/private pages unnecessarily. If browser automation is used, follow the user's session policy and preserve existing sessions/tabs; do not launch or replace a session without the authority that requires. Fixed-source collection uses anonymous HTTP and no browser.

### Optional shopping integration

The bundle ships its own comparison contract in `schemas/weekend-output.md`, section "Pass-shopping handoff". No separately installed skill is required. If an appropriate shopping skill is available, read its actual entry point and accept only compatible minimal inputs and permitted effects. If it is absent, this agent owns public comparison under the same contract: direct/no-pass baseline, the desired feasible basket, admission-band mapping, total mandatory charges, exclusions, activation/expiry, reservations, cancellation/return rules and evidence limits. Keep unavailable or protected inputs unknown; never fill them with invented totals or eligibility.

## Key Concepts

A capability is an observed usable interface with a known output boundary. A skill name, installed connector or successful transport response does not establish safe private-data access or reservation authority.

## Decision Criteria

Use a checked dated plan only when supported permitted results establish trip fit and current operational/weather coverage. Otherwise deliver a useful explicitly provisional result. Missing optional shopping integration does not block public comparison when the current agent has the necessary public evidence.

## Constraints & Limits

This package supplies no vault, privacy sandbox, forecast engine, booking interface or account connection. Planning and public comparison never imply purchases, messages, bookings or reminders.

## Common Patterns

With policy-permitted deliberately supplied dates, match official event/forecast coverage directly and label live capacity according to what was actually checked. When the caller's policy protects dates and no safe matching interface exists, research public choices, retrieve current official forecast coverage, compare conditional admissions and label trip-date fit unknown.
