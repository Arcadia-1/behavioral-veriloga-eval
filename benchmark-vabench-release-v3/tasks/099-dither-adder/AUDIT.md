# Measurement Instrumentation Audit: Task 099 Dither Adder

## Gate 1

- Label: `independent_l1_ready`.
- Function boundary: standalone differential dither injection block with a
  voltage-coded polarity input, symmetric differential offset, and preserved
  common mode.
- Counting note: independent L1 support component; it is also reused by the
  gain-extraction measurement flow.

## Gate 2

- Status: `cadence_modeling_ready`.
- Prompt hygiene: public prompt names only `dither_adder.va` as the graded
  artifact and removes private-hook language.
- Metadata repair: release metadata now targets only `dither_adder.va`; the
  stale multi-artifact L2 target list was removed.
- Modeling repair: the dither polarity target is updated on events and smoothed
  with a short explicit transition, avoiding a discrete expression directly
  driving analog contributions.
- Checker alignment: the checker ignores DPN transition guard samples and
  measures steady high/low dither sign plus common-mode preservation.

## Validation

- AHDL-style preflight: PASS with 0 diagnostics.
- EVAS reference/negative sweep: reference PASS; 5/5 negatives rejected.
- Spectre private-split reference audit: PASS.
