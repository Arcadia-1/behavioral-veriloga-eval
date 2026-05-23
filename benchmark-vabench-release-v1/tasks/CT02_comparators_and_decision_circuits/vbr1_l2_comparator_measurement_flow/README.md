# Single-ramp comparator offset measurement flow

- Entry: `vbr1_l2_comparator_measurement_flow`
- Level: `L2`
- Category: `Comparators and Decision Circuits`
- Package status: `selected_l2_target`
- Score surface: `benchmark-e2e`
- Benchmark score: `enabled`
- Materialized forms: `e2e, tb`
- Missing forms: `none`
- Certification: static `pass`; EVAS `pending`; Spectre `pending`
- Evidence: `benchmark-vabench-release-v1/reports/dual_certification.json`

This release entry is materialized in the paper-facing vaBench release package.
`release_entry.json` is the structured source of truth for forms, scoring, and certification status.
This L2 task models a single-ramp comparator offset measurement flow: a controlled input ramp drives the comparator, then the flow latches the trip voltage, estimates the input-referred offset, and asserts a validity flag. Fresh EVAS/Spectre dual validation is required after the prompt/checker/gold redesign.
