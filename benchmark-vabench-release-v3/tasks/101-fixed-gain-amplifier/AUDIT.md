# Measurement Instrumentation Audit: Task 101 Fixed Gain Amplifier

## Gate 1

- Label: `independent_l1_ready`.
- Function boundary: standalone differential fixed-gain amplifier with output
  common-mode centered at `vdd/2`.
- Counting note: independent L1 support component; it is also reused by the
  gain-extraction measurement flow.

## Gate 2

- Status: `cadence_modeling_ready`.
- Prompt hygiene: public prompt names only `gain_amp_fixed.va` as the graded
  artifact and avoids private-hook wording.
- Metadata repair: release metadata now targets only `gain_amp_fixed.va`; the
  stale multi-artifact L2 target list was removed.
- Modeling repair: debug `$strobe` output was removed from the reference model.
- Checker alignment: checker measures differential gain and common-mode
  preservation from public waveforms.

## Validation

- AHDL-style preflight: PASS with 0 diagnostics.
- EVAS reference/negative sweep: reference PASS; 5/5 negatives rejected.
- Spectre private-split reference audit: PASS.
