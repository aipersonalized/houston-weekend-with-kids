# Houston Public Sources

Collect the reviewed official Houston planning pages and check saved-source integrity for humans and agents.

## Quick Start

From the skill root:

```sh
python -B scripts/public_sources.py --refresh --dry-run --json --no-input
python -B scripts/public_sources.py --help
```

From the skill root, read `schemas/command-rules.md` in full before collection or interpreting results.

## What It Does

- Retrieve complete fixed public HTML pages and derived searchable text.
- Refresh the same corpus paths with source provenance and explicit failures.
- Check local hashes and source accounting without network or writes.
- Serialize refresh writers with an exclusive per-corpus lock so subset refreshes retain each other's inventory entries.

It uses no cookies, accounts, private inputs or browser. It cannot check private-trip availability or make reservations. Local file integrity does not establish remote freshness or source fidelity.

## Requirements

Python 3.14, standard library only. Select that interpreter explicitly; uv may be used if already available but is optional. Refresh requires Internet access. No browser or provider account is needed. A fresh package has no corpus; generate one before expecting `--check` to pass. Follow publisher terms for source material and keep generated copies local/Git-ignored.

## Examples

```sh
python -B scripts/public_sources.py --refresh --dry-run --json
python -B scripts/public_sources.py --refresh --source space-guide --json --no-input
python -B scripts/public_sources.py --check --source space-guide --json --no-input
```

Exit 0 means the requested selected action completed; 1 means source/check/runtime failure; 2 invalid input; 130 interruption. Read per-source statuses and retry only affected reviewed IDs after resolving the condition. Refresh writes only this bundle's local corpus and retains previous good bytes on retrieval failure. It creates no maintenance report or documentation database.
