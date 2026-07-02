# Audit: 117-bipolar-dac-4b-continuous

- Gate 1: `independent_l1_ready` after repair. This is a standalone continuous bipolar 4-bit DAC, distinct from scalar unipolar weighted DAC rows.
- Gate 2: `cadence_modeling_ready` for the audited hidden/negative evidence slice. EVAS2 hidden gold and Spectre AX hidden gold pass.
- AHDL lint/read-in triage: Spectre hidden gold and hidden negative logs were inspected for `AHDLLINT-*`, `VACOMP-1116`, and `VACOMP/SPECTRE` errors; none are present. Remaining setup notices are environment/Spectre X warnings, not task-specific AHDL lint failures.
- Public prompt: rewritten as a public bipolar DAC contract with interface, parameters, endpoint/step transfer behavior, and modeling constraints.
- Hidden coverage: repaired to use a distinct private code sequence from the visible smoke deck.
- Checker: generalized to derive expected `vout` from the observed input bits, including monotonicity and low/high code coverage.
- Negative evidence: 4/4 Spectre hidden negatives are behaviorally rejected.
- Human review focus: confirm that this should remain counted as a bipolar DAC, not merged into generic binary-weighted DAC coverage.
