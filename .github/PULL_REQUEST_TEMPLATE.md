## What this changes

<!-- One or two sentences. Link the issue it comes from, for example "Closes #123". -->

## Kind of change

- [ ] Wording fix, no rule changes (patch)
- [ ] Addition or clarification that breaks no valid record (minor)
- [ ] Breaks some currently valid records (major: needs 12 months' notice and a migration note)
- [ ] Add-on (optional extension; the Standard itself is unchanged)
- [ ] Repository or tooling only

## Protected parts touched (the Steward's approval is needed)

- [ ] §5 Record lifecycle
- [ ] §6, including the decision-record schema and §6.2.3.1 / §6.2.3.2
- [ ] §7 Conformance levels
- [ ] §11, Appendix G or Companion A
- [ ] "What this is not" wording, NOTICE or the licence files
- [ ] Reference files under `standard/`
- [ ] The automated checks (`tools/`, `tests/`, `.github/`) or `spec/editions.json`
- [ ] None of the above

## If the text or the reference files change

- [ ] `current_sha256` in `spec/editions.json` is updated for every document whose text changed
- [ ] The text and the reference files agree after this change
- [ ] A known defect this fixes is marked `fixed` in `tests/known-defects/cases.json`
- [ ] Release-note line written (what changes, and what now fails, if anything)

## Contributor checklist

- [ ] Every commit has a `Signed-off-by:` line (`git commit -s`), certifying the Developer Certificate of Origin 1.1
- [ ] I understand my contribution is licensed under the licence of the folder it changes (see NOTICE)
- [ ] I have said whether a substantial part was generated with an AI tool, and named anyone else who helped
- [ ] Nothing here says that following the Standard makes anyone certified or compliant
