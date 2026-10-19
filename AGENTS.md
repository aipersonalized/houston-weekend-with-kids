# Houston Weekend Skill Repository Guide

## Purpose and Scope

This repository distributes a portable Houston family-planning Agent Skill and an optional Claude Code plugin wrapper. Keep family connection, realistic pacing and reliable public evidence at the center of changes.

## Working Rules

- Inspect current files and Git changes before editing; preserve unrelated work.
- Keep the portable core self-contained under `skills/houston-weekend-with-kids/`. Host-specific packaging belongs outside it.
- Preserve live local discovery, explicit weather coverage and the distinction between provisional plans, checked facts and reservations.
- Do not store personal trip records, private dates, account details, credentials or private access/health needs in this repository.
- Read the affected command and capability contracts before running tools. Publication and other external actions need authority from the actual request.

## Conventions and Contracts

Use relative resource paths, descriptive lowercase filenames and `America/Chicago` for Houston public timed examples. Maintain source URLs and observation dates. No provider-specific tool names or absolute installation paths belong in the core.

## Operational Cautions

The optional collector uses fixed public HTTPS sources without browser sessions. Generated `corpus/` contains third-party works and remains local/ignored. Do not commit personal records, generated source copies, local tooling or documentation databases.

## Commands and Validation

From `skills/houston-weekend-with-kids/`, with Python 3.14:

```sh
python -B scripts/public_sources.py --refresh --dry-run --json --no-input
python -B -m unittest discover -s evals -p test_public_sources.py
```

Preview performs no network/writes. Tests use synthetic fixtures and mocked retrieval. Read `schemas/command-rules.md` for refresh effects. From the repository root, `claude plugin validate .` checks the optional Claude wrapper when Claude Code is installed. Acceptance also needs local-link/metadata review, source fidelity and relevant static scenario walkthroughs; these commands do not prove model performance.

## Workspace Map

- [README.md](README.md): installation, use and compatibility limits.
- [SKILL.md](skills/houston-weekend-with-kids/SKILL.md): routing and completion contract.
- [Maintenance guide](skills/houston-weekend-with-kids/skill-ci/README.md): review and improvement criteria.
- [LICENSE](LICENSE): MIT terms for authored files.
- `.claude-plugin/`: optional Claude plugin and marketplace metadata.

## Environment and Dependencies

Planning uses the host's file-reading and public-web capabilities. The optional collector requires Python 3.14 and no third-party packages. No account, provider API key or private-data adapter is bundled.
