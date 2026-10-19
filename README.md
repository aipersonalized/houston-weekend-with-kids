# Houston Weekend With Kids

An AI provider agnostic [Agent Skill](https://agentskills.io/specification) for planning a Houston weekend with children. Find neighborhood activities, community events and major attractions, check official weather, and leave room for meals, breaks and time together.

The result is a practical two-day outline with sources, admission dependencies, indoor alternatives and honest unknowns. Attraction passes are compared only against places the family actually wants and can visit.

## Install

Clone or download this repository:

```sh
git clone https://github.com/aipersonalized/houston-weekend-with-kids.git
```

Copy the complete `skills/houston-weekend-with-kids/` directory into your agent's supported skill directory. Keep the folder name and its bundled resources together. Follow your host's current instructions to discover or reload skills; directory locations and activation differ by host. A host without skill discovery can read `SKILL.md` and the linked resources directly.

The core has no model, AI provider, API key, account or MCP server dependency. Your agent needs a way to read files and research public web pages for current events, venue rules and weather. Python is optional for the source utility; it is unnecessary for ordinary planning. This repository does not supply a private-data or reservation adapter.

### Optional Claude Code plugin

The `.claude-plugin/` files are a Claude Code adapter around the same portable core. They are not a universal plugin format. In Claude Code:

```text
/plugin marketplace add aipersonalized/houston-weekend-with-kids
/plugin install houston-weekend-with-kids@aipersonalized-houston-skills
```

Use the host's plugin reload/restart instructions after installation. For a local development checkout, start Claude Code with `claude --plugin-dir ./houston-weekend-with-kids`. See the official [plugin reference](https://code.claude.com/docs/en/plugins-reference) and [marketplace instructions](https://code.claude.com/docs/en/plugin-marketplaces).

## Use

Ask your agent, for example:

> Suggest a relaxed Houston weekend with kids who enjoy space and hands-on art. Include neighborhood activities and an indoor alternative. Keep dates provisional, and check the current public forecast's coverage.

Or:

> Compare a museum-focused day with a local workshop and park day. Explain the travel and break assumptions before discussing attraction passes.

The skill asks only for consequential missing inputs. Planning dates, anonymous admission categories, interests, adult count and budget can be deliberately supplied when your privacy policy permits. Names, birthdates, exact addresses and booking/account identifiers are unnecessary. If your policy protects travel dates or other details from model context, keep them in supported local tools and use bounded fit results; without that interface, affected planning stays conditional. Read the [privacy and capability contract](skills/houston-weekend-with-kids/references/privacy-and-capabilities.md).

Planning does not book, buy, send messages or hold tickets. Current research, an estimated itinerary, live availability and a completed reservation are separate states.

## Package

```text
.claude-plugin/                 Optional Claude Code plugin + marketplace
skills/houston-weekend-with-kids/
  SKILL.md                     Portable entry point
  LICENSE                      MIT terms travel with the copied skill
  playbooks/                   Discovery → weather → venue checks → plan
  references/                  Houston background and capability boundaries
  schemas/                     Planning output and command contracts
  assets/source-catalog.json   Eight official background source URLs
  scripts/                     Optional Python standard-library utilities
  evals/                       Deterministic source-tool tests
  skill-ci/                    Maintenance and evaluation guidance
```

## Optional source utility

Requires Python 3.14; tested on Windows with Python 3.14. It uses the standard library only. From `skills/houston-weekend-with-kids/`:

```sh
python -B scripts/public_sources.py --refresh --dry-run --json --no-input
python -B -m unittest discover -s evals -p test_public_sources.py
```

The preview makes no network requests or file changes. Read [command rules](skills/houston-weekend-with-kids/schemas/command-rules.md) before refreshing sources. A refresh downloads the fixed official source set into a local, Git-ignored `corpus/`; `--check` checks those local copies. A fresh clone has no saved corpus, so `--check` correctly reports missing copies until a refresh succeeds. The utility does not discover events, retrieve weather, use browser sessions or verify ticket capacity.

Venue pages are third-party works. Full HTML/text copies are generated locally and are not distributed by this repository or covered by its MIT license. Follow the source publisher's terms before collecting, reusing or redistributing their material. Background guidance was last reviewed on 2026-10-18; recheck current official rules for actual decisions.

## Compatibility and limits

The core follows the Agent Skills format. The optional plugin uses Claude Code's documented layout. Static format checks, local plugin validation and deterministic utility tests do not establish itinerary quality across models or installation on every host. No hosted model planning trials or live reservation tests are claimed. Public-web access and supported private-data handling depend on your host.

For corrections, open a [GitHub issue](https://github.com/aipersonalized/houston-weekend-with-kids/issues) with public, non-sensitive details. Include the affected rule/source and expected behavior. Do not post family records, private travel plans, account details or credentials.

## Support this project

If this skill helps your family spend time together, you can optionally [buy me a coffee](https://buymeacoffee.com/aipersonalized). Support is voluntary; the skill remains free to use under its MIT license.

## License

Authored instructions and code are [MIT licensed](LICENSE). External websites, venue names and third-party content retain their owners' rights. This project is independent of the listed venues, weather services and AI providers.
