# The Decision Provenance Standard™

**Version**: 1.0 — Reading Edition (rev. 8 — 2026-05-30)
**Date of base text**: 2026-04-30 (v1.0 integration close)
**Date of rev. 4 deltas**: 2026-05-06
**Date of rev. 5 deltas**: 2026-05-09
**Date of rev. 6 deltas**: 2026-05-15
**Date of rev. 6.5 deltas**: 2026-05-18
**Reading Edition (rev. 8)**: 2026-05-30 — readability + de-defensiveness + thinning + genericization (the Standard reads as a standalone generic standard, decoupled from any companion book or reference-implementation product name in normative text). Conformance contract UNCHANGED from v1.0 (no field, lifecycle-state, enum, conformance-level, or signal-definition change). The Standard is restructured into a normative core plus Companion A (Regulatory Cross-References), Companion B (Worked Charter Library), Companion C (Implementation Guidance), and Appendix G (Governance and References).
**Author**: Yohay Etsion (Founding Steward)
**Steward**: Etsion Brands Ltd. (institutional Steward, Israeli holding company)
**License**: Creative Commons Attribution 4.0 International (CC-BY 4.0)
**Status**: Open standard. Not a certified product. Not legal advice. Not a regulatory substitute.

---

> ⚠️ **Not legal advice.** This Standard is a drafting and triage aid produced under the Etsion Brands Ltd. Steward role. It is not counsel. No attorney-client relationship is created by its production, distribution, or use. Jurisdiction-specific questions, contested matters, and any decision with material legal or regulatory consequences require review by a licensed attorney in the relevant jurisdiction. Do not rely on this Standard as the sole basis for any legal, compliance, or employment decision.
>
> **Jurisdiction Assumed**: U.S. federal + Delaware as primary; United Kingdom (England & Wales for litigation framing), the European Union (with the EU AI Act, Regulation (EU) 2024/1689, as the load-bearing AI-specific framework), and the State of Israel as named secondaries. Where a deployer's Charter, decision records, or governance posture concerns a different jurisdiction, every requirement, definition, and conformance signal in this Standard is to be treated as a hypothesis to verify with local counsel.

---

## About This Standard

The Decision Provenance Standard™ is an open standard for the production and maintenance of audit-ready decision provenance in organizations that dispatch consequential decisions through a mix of human and AI authorship. It is an open record format published under the Creative Commons Attribution 4.0 International License (CC-BY 4.0), authored by Yohay Etsion as Founding Steward under the institutional Steward role held by Etsion Brands Ltd.

By design, there is no certification track and no certifying body: every conformance level is self-declared, which keeps the Standard open infrastructure rather than a gated regime (self-declared / no-certifying-body posture treated authoritatively at §7 and §11.2). The trademark on the name is separate from the CC-BY 4.0 license on the text: per the Creative Commons license terms (Section 2(c) of the CC-BY 4.0 legal code: "Patent and trademark rights are not licensed under this Public License"), trademark rights are not licensed with the text, so anyone may use, extend, and fork the text under attribution while the name stays protected against misrepresentation (full trademark convention at §11.1).

A working open-source reference implementation is published under the MIT License and is described in Appendix G §12.4; it is a real artifact that readers may consult, but it is not the Standard and the Standard does not depend on it.

The Standard's central term, "audit-ready decision provenance," is defined and firewalled at §1.4.1; the locked definition and its load-bearing UPL firewall are stated authoritatively there.

### Normative Keywords (RFC 2119)

The key words **"MUST"**, **"MUST NOT"**, **"REQUIRED"**, **"SHALL"**, **"SHALL NOT"**, **"SHOULD"**, **"SHOULD NOT"**, **"RECOMMENDED"**, **"MAY"**, and **"OPTIONAL"** in this document are to be interpreted as described in IETF RFC 2119 (Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels," BCP 14, RFC 2119, March 1997, <https://www.rfc-editor.org/rfc/rfc2119>). Where these keywords appear in normative text, they carry the RFC 2119 meaning. Where they appear in lower-case or in non-normative explanatory prose, they carry their ordinary English meaning. The Standard is otherwise normative throughout, in the sense that every requirement, field definition, lifecycle state, and conformance criterion is structural and binding on a Charter or decision record that claims conformance under §7; the RFC 2119 keyword declaration governs only the explicit-level discipline of "MUST" / "SHOULD" / "MAY" within that normative envelope.

The full RFC 2119 citation appears in Appendix G (References) §12.2.4.

---

## Table of Contents

1. **Section 1** — Preamble and Scope
2. **Section 2** — Definitions
3. **Section 3** — The Charter Mechanism
4. **Section 4** — Authority and Authorship in AI-Mediated Decisions
5. **Section 5** — Record Lifecycle States
6. **Section 6** — The Required Artifact Set
7. **Section 7** — Conformance Levels
8. **Section 8** — Regulatory Cross-References
9. **Section 9** — Worked Examples
10. **Section 10** — Implementation Guidance
11. **Section 11** — Trademark, Governance, and Voluntary Adoption
12. **Section 12** — References

## List of Figures

The figures are explanatory aids, not normative. Each is collected with its full text-alternative in **Companion D — Diagrams**.

| Figure | Title | Illustrates |
|---|---|---|
| Figure 3-1 | Charter Lifecycle State Machine | §3.3 |
| Figure 3-2 | Mode Dispatch Grammar and the Embedded-Mode-2 Edge Case | §3.4 |
| Figure 4-1 | Article 50 Disclosure-Metadata Flow | §4.6.2 |
| Figure 4-2 | Mode-Drift Four-Layer Composed Mitigation | §4.8.1 |
| Figure 4-3 | Emission-Cadence by Semantic Class | §4.8.2 |
| Figure 5-1 | Decision-Record State Machine: Two Distinct State Families | §5.1 / §6.2 |
| Figure 6-1 | Artifact-Set Relationship Map | §3 (orientation) |
| Figure 7-1 | The Three Conformance Levels: Cumulative Criteria | §7.2 |

---

