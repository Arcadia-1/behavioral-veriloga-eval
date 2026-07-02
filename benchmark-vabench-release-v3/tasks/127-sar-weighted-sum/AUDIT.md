# Audit: 127-sar-weighted-sum

## Gate 1

- Label: `independent_l1_ready`.
- Function: voltage-domain SAR residue/weighted-sum source with a non-binary
  split decision boundary.
- Independence: retained as distinct from generic weighted decoder/DAC rows
  because `D7`/`D6` split the next binary step in a 5:3 ratio and the output is
  a bipolar SAR residue source rather than a conventional unipolar DAC decode.

## Gate 2

- Status: `cadence_modeling_ready`.
- Prompt hygiene: replaced the direct full expression with a public weighting
  contract, endpoint behavior, and modeling constraints.
- Public contract now exposes bit order, threshold, coarse/binary/split-tail
  weighting structure, 512-unit bipolar normalization, monotonicity, and
  all-low/all-high endpoint behavior.
- Visible/hidden relationship: hidden testbench is no longer byte-identical to
  visible smoke; hidden coverage isolates the `D6` and `D7` split weights before
  exercising `D10` and the all-high endpoint.
- Checker: `v3_sar_weighted_sum`, stable samples for all-low, isolated split
  weights, coarse bit, and all-high endpoint.
- Functional sanity vectors:
  - all inputs low: `VOUT=-1`.
  - isolated `D6`: `VOUT=-0.90625`.
  - isolated `D7`: `VOUT=-0.84375`.
  - isolated `D10`: `VOUT=-0.125`.
  - all inputs high: `VOUT=0.998046875`.
- Cadence reference correspondence: Cadence DAC examples expose clock/event,
  threshold, bit order, full-scale scaling, and transition behavior as public
  model contracts; this task keeps the same public-contract principle while
  using scalar ports instead of a variable-width bus.

## Validation

- EVAS hidden gold: PASS.
- EVAS negative variants: 4/4 rejected.
- Spectre hidden gold: PASS.
- Spectre negative variants: 4/4 rejected.
- AHDL lint triage: no `AHDLLINT-*` findings. Spectre reported only
  `VACOMP-2435` and `SPECTRE-592` environment/mode warnings.
