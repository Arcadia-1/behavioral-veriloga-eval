# Honest SOP Audit: Task 096 Converter Static Linearity Measurement

## Scope

Task boundary is the primary Verilog-A DUT artifact
`converter_static_linearity_measurement_flow.va`, migrated from the
`vbr1_l2_converter_static_linearity_measurement_flow` scenario. Companion SCS
stimulus is supplied by the harness.

## Gate Status

- Gate 1: `l2_measurement_ready`. This is a converter measurement-flow block,
  not a standalone ADC or DAC core. It samples a converter sweep, exposes a
  4-bit code metric, reconstructs a deliberately non-ideal DAC level, and
  produces DNL/INL-like voltage metrics from the observed history.
- Gate 2: `cadence_modeling_ready` for the current assets. The public prompt
  now states the target artifact, interface, parameter contract, measurement
  behavior, and voltage-domain constraints without hidden-evaluator wording.

## Checker And Evidence

- Source checker id: `vbr1_l2_converter_static_linearity_measurement_flow_tb`.
- EVAS closeout sweep: gold PASS; `neg_001_zero` rejected.
- Spectre closeout: visible gold PASS, hidden gold PASS, and hidden
  `neg_001_zero` rejected.
- AHDL triage: no task-level `AHDLLINT-*` messages or AHDL compile errors were
  observed in the closeout runs; only the global `VACOMP-2435` environment
  warning appears.

## Remaining Risk

This migrated L2 row currently has one hand-authored negative variant. It is
usable for the reviewed data-converter surface, but future strengthening could
add more negatives for wrong DNL scaling, flat INL, or non-monotonic
reconstruction.
