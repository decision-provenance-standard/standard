# Reference Implementation — Release Notes

**Release label**: v5.1.0
**Directory path**: `standard/v5.0/` (unchanged so the Standard's `standard/v5.0/...` references resolve; v5.1.0 is the version label, the path stays `v5.0/`)
**Aligned to**: Decision Provenance Standard, rev. 8

---

## What This Release Is

This is the runnable reference implementation of the Decision Provenance Standard's conformance reporter at Conformance Level 3. It is aligned field-for-field and signal-for-signal to the Standard's normative text. The Standard is authoritative; this implementation tracks it.

The implementation records process. It does not certify, ensure, or substitute for any regulator or auditor review. Conformance to the Standard is self-declared by the implementer; no body certifies it.

---

## What It Contains

- **23-signal conformance vocabulary** — Level split: 6 Level 1 (Charter structural completeness) + 13 Level 2 (decision-record discipline) + 4 Level 3 (continuously auditable). The vocabulary is the locked enumeration the reporter API validates `evidence_metric` against, identical between `conformance/signal-vocabulary.md` and the OpenAPI `evidence_metric` enum.
- **3-value `dispatch_mode` enum** — `mode-1`, `mode-2`, `mode-1-with-embedded-mode-2-summary`. Exhaustive; no fourth mode.
- **5-field Article 50 disclosure schema** — `declaring_authority`, `ai_system_identity`, `jurisdictional_applicability`, `content_type_tag`, `generation_timestamp`, plus permitted implementation extras tolerated by the conformance check.
- **Mode-drift four-layer composed mitigation** — Layer 1 statistical detection (detection-only scaffolding at first release), Layer 2 in-flow 4-question audit hook (hard gate at Mode-1 record close), Layer 3 Mode-Confirmation Audit primitive (peer-review confirmation), Layer 4 named human attestation (structured `mode_classification_attestation` object at close).
- **Two state machines** — Charter 5-state forward-only lifecycle + `review-required` RECORD-state interrupt; decision-record `dispatched / drafted / closed` lifecycle with the two deliberately-distinct §5.1-lifecycle and §6.2-dispatch state families.
- **Reporter API** — single-write `POST /dps/conformance/charter-escalation` endpoint (OAuth 2.0 client_credentials, idempotency-key, synchronous ack-only, standardized error envelope, rate limiting, JSON Schema Draft 2020-12 validation).
- **Cross-stream conformance test apparatus** — synthetic Charter library + category test matrix asserting 1:1 alignment between the Standard's normative text and the implementation's runnable behavior.

---

## Versioning

This release carries the label **v5.1.0**. The directory path remains `standard/v5.0/` so the Standard's `standard/v5.0/...` references resolve; the version label and the directory path are deliberately distinct. Conformance-contract changes (signal vocabulary, schema field names, reporter wire contract) are additive at the schema and enum level and follow semantic-version discipline; breaking changes to the contract require a major-version bump and steward review.

---

## Licensing

The Decision Provenance Standard text is licensed CC-BY 4.0. This reference-implementation code is licensed MIT.

---

*Reference implementation aligned to the Decision Provenance Standard, rev. 8.*
