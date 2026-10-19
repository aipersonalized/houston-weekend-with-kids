# Command Rules

## When to read this

Read this file in full before running public-source or step-list commands and before interpreting their results. These optional utilities are separate from ordinary planning and supply no private-data adapter.

## Inputs and outputs

Run from this skill root using Python 3.14. Commands below use `python`; if multiple interpreters are installed, select Python 3.14 explicitly (for example, `uv run --python 3.14 python -B ...` when uv is already available). No package installation or uv dependency is required. Public-source operations use the standard library only, run once without prompts and never attach or launch a browser.

### Public source collection

```sh
python -B scripts/public_sources.py --help
python -B scripts/public_sources.py --refresh --dry-run --json
python -B scripts/public_sources.py --refresh --json --no-input
python -B scripts/public_sources.py --refresh --source space-guide --json --no-input
python -B scripts/public_sources.py --check --json --no-input
```

Choose exactly one of `--check` or `--refresh`. Optional repeatable `--source` accepts only fixed reviewed IDs in `assets/source-catalog.json`; default selects all eight pages. It does not accept URLs, private values, dates, addresses or arbitrary output paths. Invalid IDs are not echoed. `--dry-run` previews without network or writes. `--verbose` sends progress to stderr; `--quiet`, `--no-input` and `--no-color` control presentation. Nonempty `NO_COLOR` suppresses default terminal color. JSON stdout is one object without banner, progress or ANSI codes.

`--refresh` retrieves complete selected public HTML responses using fixed HTTPS URLs without cookies or browser access. Same-official-host redirects are allowed after validation. It writes `corpus/sources/<reviewed-id>.html`, derived `.txt`, `corpus/inventory.json` and the temporary refresh lock described below; it creates no maintenance report. Linked assets/scripts and dynamic checkout are excluded. It uses bounded timeout/retry, validates markers and complete HTML, preserves previous good source bytes on retrieval failure, and marks failed source metadata explicitly. Repeated refresh replaces the same local paths rather than storing source-version history; generated copies remain Git-ignored. Original bytes are not claimed to include content rendered by JavaScript or referenced assets.

Refresh also creates an exclusive `corpus/.refresh.lock` before reading the inventory and holds it through source/inventory publication. A competing refresh fails without requests or changes to existing source/inventory data; retry only after the current writer finishes. Normal completion or interruption removes only its own lock. Help, preview and local check create no lock or directories and do not modify an existing lock. A hard process termination may leave the lock: verify that no refresh is active, verify the exact lock path is inside this skill's corpus, then remove only that stale lock. Do not auto-clear locks by age or delete a lock held by another writer. The check can observe an in-progress refresh and fail transiently; wait for the writer to finish before interpreting that result.

`--check` reads local catalog/inventory/source files only and checks declared source state and hashes. It does not write, contact sites, assess source fidelity, check future hours or prove capacity. A fresh package has no corpus and correctly fails this check until sources are collected. Generated third-party source copies stay local and Git-ignored; they are not covered by the authored MIT license. Follow publisher terms. A passing hash requires separate content review before using a new or changed source.

JSON contains `ok`, `action`, per-source `id` and `status`, and a limitations statement. Refresh/check failures include a bounded reason; no response body or raw backend error is emitted. Preview contains selected IDs and explicit no-network/no-write indicators. Inventory owns source URLs, publisher/title, retrieval timestamp, unknown publisher version, file mappings, representations, hashes and failure state. Integrity hashes are not a privacy mechanism or substitute for Git history.

### Step discovery

```sh
python -B scripts/list_skill_steps.py
```

Takes no arguments. Reads this bundle's playbooks and prints their numbered steps as text. Exit 0 means successful extraction; exit 1 means missing/unreadable playbooks or parse failure. It does not execute the workflow, write files or qualify behavior.

### Deterministic tests

```sh
python -B -m unittest discover -s evals -p test_public_sources.py
```

Uses synthetic public fixtures in disposable temporary directories and mocks network calls. It performs no live request or personal-data access. Exit 0 means these implemented boundaries passed, without establishing model behavior or current remote availability.

## Checks and failures

Public-source exit codes: 0 completed selected action, 1 source/integrity/runtime failure, 2 invalid arguments/source ID, 130 interruption. Argparse usage errors return 2 and help returns 0 before work. A partial collection returns 1 with individual statuses. Correct the named condition, inspect preserved files and retry affected IDs only; do not treat failure as an exclusion or silently replace a source with marketing/navigation.

Valid example: `--refresh --source space-guide --dry-run --json`. Invalid example: `--refresh --source unknown --json`; this returns 2 without network/writes. A changed or missing local source returns 1 on `--check`. Review its provenance and exact source, then refresh only the affected reviewed ID. If official content cannot be obtained, disclose the gap and withhold dependent claims. Do not work around failures by launching a fresh browser or probing accounts.
