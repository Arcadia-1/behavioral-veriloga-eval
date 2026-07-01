# Audit: 295-clocked-adc3bit

- Gate 1: `independent_l1_ready` after rescue. This is retained as a clocked 3-bit ADC with explicit voltage bit-bus outputs.
- Gate 2: `cadence_modeling_ready` for the audited hidden/negative evidence slice. EVAS2 hidden gold and Spectre AX hidden gold pass.
- AHDL lint/read-in triage: Spectre hidden gold and hidden negative logs were inspected for `AHDLLINT-*`, `VACOMP-1116`, and `VACOMP/SPECTRE` errors; none are present. Remaining setup notices are environment/Spectre X warnings, not task-specific AHDL lint failures.
- Public prompt: rewritten to expose rising-edge sampling, uniform-bin quantization, clipping, output bit order, and bit rail levels.
- Hidden coverage: repaired to include negative-range clipping, interior codes, and high-end clipping distinct from visible smoke.
- Checker: generalized to derive expected `vd2/vd1/vd0` rails from sampled `vin`.
- Negative evidence: 4/4 Spectre hidden negatives are behaviorally rejected.
- Human review focus: confirm the bit-bus output interface makes this distinct from scalar-code ADC `167` and track/convert ADC `195`.
