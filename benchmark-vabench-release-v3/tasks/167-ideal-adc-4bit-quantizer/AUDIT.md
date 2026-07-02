# Audit: 167-ideal-adc-4bit-quantizer

- Gate 1: `independent_l1_ready` after repair. This is a differential-input ADC that emits a scalar analog code.
- Gate 2: `cadence_modeling_ready` for the audited hidden/negative evidence slice. EVAS2 hidden gold and Spectre AX hidden gold pass.
- AHDL lint/read-in triage: Spectre hidden gold and hidden negative logs were inspected for `AHDLLINT-*`, `VACOMP-1116`, and `VACOMP/SPECTRE` errors; none are present. Remaining setup notices are environment/Spectre X warnings, not task-specific AHDL lint failures.
- Public prompt: expanded to expose the differential input, rising-edge sampling, uniform threshold-count quantizer contract, and output code semantics.
- Hidden coverage: repaired to use a distinct differential stimulus with nonzero `vin`.
- Checker: generalized to derive the expected scalar code from sampled `V(vip)-V(vin)`.
- Negative evidence: 4/4 Spectre hidden negatives are behaviorally rejected.
- Human review focus: confirm this remains distinct from bit-bus ADC rows such as `295`.
