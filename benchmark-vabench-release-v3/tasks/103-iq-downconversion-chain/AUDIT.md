# Two-Gate Audit: Task 103 IQ Downconversion Chain

## Gate 1: Admission

- Label: `l2_core_ready`.
- Human-review status: proposed for retention as an RF/AFE I/Q downconversion
  L2 row.
- Function boundary: a composed receiver macromodel with quadrature LO phase
  sequencing, I/Q LO monitors, two mixer paths, bounded I/Q baseband
  observables, and a phase monitor.
- Duplicate check: distinct from the single mixer row because it evaluates a
  four-state quadrature chain with two mixer paths and I/Q observability rather
  than one polarity-controlled baseband output.

## Gate 2: Modeling And Evidence

- Status: `cadence_modeling_ready`.
- Prompt hygiene: public prompt now states the DUT interface and observable I/Q
  chain behavior directly. Migration history, hidden-evaluator wording, and
  testbench-generation text were removed.
- Cadence/Verilog-A correspondence: the model uses event-updated phase state,
  voltage-coded I/Q monitor outputs, bounded mixer targets, and `transition()`
  smoothing. Stored quadrature phase is documented as transient behavioral
  state, not a Spectre RF/PSS claim.
- Visible/hidden coverage: hidden stimulus now differs from visible by RF
  envelope levels while still exercising positive I, positive Q, negative I,
  negative Q, and common-mode return windows.
- Checker strength: checker requires positive and negative quadrature output
  windows, four-state phase monitor ordering, I/Q LO polarity monitors, mixer
  monitor polarity and common-mode return when the input envelope returns to
  common mode.
- Negatives: 5/5 concrete variants reject behaviorally under EVAS.
- EVAS evidence: hidden gold PASS; concrete negatives 5/5 rejected with
  `FAIL_SIM_CORRECTNESS`.
- Spectre evidence: hidden gold PASS under the RF/AFE remaining review rerun.
- AHDL lint status: EVAS AHDL-like lint preflight PASS with zero diagnostics.

## Residual Risk

Spectre negatives were not rerun for every concrete negative variant in this
category closeout. The row is a transient voltage-domain behavioral I/Q
downconversion chain, not a transistor-level RF receiver or RF/PSS-ready model.
