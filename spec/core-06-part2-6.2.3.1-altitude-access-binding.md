### 6.2.3.1 Access-policy binding for the altitude field

The `altitude` field is not a documentation field. A conformant deployer's access-policy layer SHALL enforce the following bindings at record-write time, record-read time, and affirmation time:

1. **Write-time binding.** A record SHALL NOT be written at `altitude: individual-professional` unless the access-policy layer has verified that (a) the Charter under which the record is authored carries a use-case scope-limit declaration per §3.1 that authorizes individual-professional altitude for the use case the record serves, AND (b) the `consent_posture.consent_record_pointer` resolves to an active (non-withdrawn) affirmer consent record per Appendix G §G.11.3.

2. **Read-time binding.** A record at `altitude: individual-professional` SHALL be readable only by the affirmer named in `affirmation_record.actor_identity` by default. Reader principals other than the affirmer SHALL be granted access only where the Charter's use-case scope-limit declaration explicitly enumerates the reader role and the deployer's IAM policy resolves the reader to that role. The default-on access posture for individual-professional altitude records is a structural failure mode and is NOT conformant.

3. **Affirmation-time binding.** An affirmation event at `altitude: individual-professional` SHALL be rejected by the access-policy layer where the `consent_posture.withdrawal_state` is `withdrawn-stream-stopped`. Affirmation events at `altitude: function-leader` or `altitude: team-leader` SHALL verify the Charter's use-case scope-limit declaration permits the altitude before sealing per §5.1(3).

The access-policy enforcement is the structural binding the schema makes load-bearing. The Charter's use-case scope-limit declaration (§3.1) is the deployer's policy artifact; the access-policy layer is where that policy becomes architecturally enforced. A deployer whose access-policy layer does not perform these bindings has departed from §6.2.3 conformance and SHALL NOT self-declare Conformance Level 2 or above per §7. The Standard does not specify the implementation mechanism; the Standard specifies the bindings any access-policy layer MUST perform. Asset 10 (IT Governance Quick Reference) §3 describes a reference implementation pattern.

The bindings apply symmetrically to AI workers: where a Mode 2 dispatch chain operates at sub-executive altitude per `drafting_authority.deployer_role_pointer`, the access-policy layer SHALL verify that the AI worker's authorized role per §1.4 dispatch grammar is in scope under the Charter's use-case scope-limit declaration at the named altitude.

