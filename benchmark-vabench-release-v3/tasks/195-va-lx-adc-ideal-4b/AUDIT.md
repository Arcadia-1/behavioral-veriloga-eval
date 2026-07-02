# Audit: 195-va-lx-adc-ideal-4b

- Gate 1: `independent_l1_ready` after repair. This is a track-then-convert four-bit SAR-style ADC with output bit rails.
- Gate 2: `cadence_modeling_ready` for the audited hidden/negative evidence slice. EVAS2 hidden gold and Spectre AX hidden gold pass.
- AHDL lint/read-in triage: Spectre hidden gold and hidden negative logs were inspected for `AHDLLINT-*`, `VACOMP-1116`, and `VACOMP/SPECTRE` errors; none are present. Remaining setup notices are environment/Spectre X warnings, not task-specific AHDL lint failures.
- Public prompt: expanded to expose track phase, falling-edge conversion, bit order, and binary-search threshold sequence.
- Hidden coverage: repaired to use a distinct tracked input sequence from visible smoke.
- Checker: generalized to derive expected bits from the tracked input before each falling clock edge.
- Negative evidence: 4/4 Spectre hidden negatives are behaviorally rejected.
- Human review focus: confirm this is distinct from scalar-code quantizer `167` and bit-bus edge ADC `295`.
