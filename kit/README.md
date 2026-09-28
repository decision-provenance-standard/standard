<!-- SPDX-License-Identifier: Apache-2.0 -->

# Declaration kit

This kit helps an organization, or the maker of a product, write its own self-declaration under the Decision Provenance Standard&trade;. It has two parts:

- **A prompt for any AI assistant** (`declaration/prompt.md`). Paste it into the chat assistant you already use. It asks you about your Charters one question at a time, works out with you which Conformance Level the evidence supports, and ends with your declaration as plain text and as a block of data.
- **A skill for coding agents** (`skill/dps-declaration/`). It reads your actual Charters and decision records in a repository, writes an evidence report, one line per criterion, and drafts the declaration from that evidence.

A Charter is the written rulebook for one area of decisions: who owns them, how they are drafted, which records are kept and where. An organization declares a Conformance Level (1, 2 or 3) for its Charters. A product declares only that it implements the Standard, with no Level.

## What the kit does not do

- **It certifies nothing.** A self-declaration is the declarer's own claim. Neither the kit nor the Standard's Steward (the organization that looks after the Standard's text) validates, grades or audits it. The declaration's own statement says so.
- **It never produces badge code.** The prompt and the skill draft the declaration for a named person at your organization to read and confirm. Only the badge page makes the badge.
- **It gives no legal advice.** It helps you describe your own records against the Standard's criteria; it says nothing about what any law requires.

## How it relates to the badge page

The badge page is at https://decisionprovenancestandard.org/badges.html. It embeds the same prompt, and checks a declaration against the same data format (`declaration/dps-declaration.schema.json`). The schema is also served at its `$id` address. When your declaration is ready, paste its data block into the badge page. It gives you one piece of code: the badge, a small "Our declaration" fold-out anyone can read, and the declaration as data.

## How to use the prompt

1. Copy everything in `declaration/prompt.md` below the two comment lines at the top into your AI assistant.
2. Answer its questions. Say where each piece of evidence is kept; a claim nobody can locate counts as "not sure".
3. Read the evidence table and the declaration it gives you. The person named in the declaration should confirm it before it is published.
4. Paste the data block into the badge page.

## How to use the skill

1. Copy the folder `skill/dps-declaration/` into the skills folder your coding agent reads. It uses the Agent Skills format: a `SKILL.md` with a `references/` folder.
2. In the repository that holds your Charters and decision records, ask the agent to "draft our Decision Provenance Standard self-declaration".
3. The agent looks first, asks only what it cannot find, and writes its files to a `decision-provenance/` folder: an evidence report for an organization, and a draft declaration when there is something to declare.
4. Check the draft against the schema, either by pasting it into the badge page or with `python -m jsonschema -i <declaration file> skill/dps-declaration/references/dps-declaration.schema.json`. Exit code 0 means it is valid, even if the command prints a warning.

## What is in this folder

| Path | What it is |
|---|---|
| `declaration/criteria.json` | The single source for the Conformance Level criteria: 25 criteria (8 for Level 1, 10 for Level 2, 7 for Level 3), each with its question, the Standard's sections and signal (the Standard's name for each check), and, where needed, a note on how to judge it |
| `declaration/dps-declaration.schema.json` | The declaration's data format, version 1 (JSON Schema 2020-12), with its fixed statements |
| `declaration/prompt.md` | The prompt for any AI assistant. Generated |
| `declaration/build.py` | Generates the prompt and the skill's references from the two sources, and checks that they match |
| `skill/dps-declaration/SKILL.md` | The coding-agent skill. Written by hand; it holds no criteria |
| `skill/dps-declaration/references/` | The criteria in readable form, and copies of `criteria.json` and the schema. Generated |

## Versions

The prompt and the skill draft declarations against version 1.2 (reading edition rev. 10) only, `"standard_version": "v1.2-rev10"`. Version 1.2 is a minor release, so a Charter that meets version 1.1 (reading edition rev. 9) also meets version 1.2. The format still accepts `"v1.1-rev9"` and `"v1.0-rev8"` for declarations already made against them.

For version 1.2 the kit added L1-08 (every record carries the fields required at its state) and L3-07 (records findable and retained as §6.4 requires), and retired L2-10: the minimum group size for team-level records is now a recommendation, shown as a note under L2-09. A retired ID is never reused.

## Changing the kit

- Edit `declaration/criteria.json` or `declaration/dps-declaration.schema.json`, then run `python kit/declaration/build.py --kit-only` from the repository root. (`SKILL.md` is written by hand and needs no build.)
- `python kit/declaration/build.py --check --kit-only` exits 1 and names every generated file that no longer matches its sources. The check "Declaration kit is in sync" runs it on every pull request.
- The badge page lives in the website's repository. It is built from the same sources by the full mode of `build.py` (without `--kit-only`), which also fills the page's generated blocks.
- The criteria follow the Standard's text. Where they differ, the text is binding.

## Known limits

- **Appendix G §G.11.3.** Appendix G is informative. Since v1.2, a requirement in §G.11.3 that no core section states reads as SHOULD, so the kit checks only the core rules and shows §G.11.3's recommendations as notes.

## License

The files in this folder are licensed under the Apache License 2.0; the license text is in [`LICENSES/Apache-2.0.txt`](../LICENSES/Apache-2.0.txt). The criteria's wording is adapted from the Standard's text, which is published under CC BY 4.0. The license gives no rights in the name "Decision Provenance Standard" or its mark; see [NOTICE](../NOTICE).
