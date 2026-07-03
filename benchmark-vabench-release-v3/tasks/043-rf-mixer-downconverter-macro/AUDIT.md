# Two-Gate Audit: Task 043 RF Mixer Downconverter Macro

## Gate 1: Admission

- Label: `independent_l1_ready`.
- Human-review status: proposed for retention as the RF/AFE category's standalone
  mixer/downconverter L1 row.
- Function boundary: a voltage-domain RF mixer macromodel that applies LO
  polarity to the RF envelope around common mode and exposes bounded baseband
  output plus an activity metric.
- Duplicate check: distinct from LNA/PA compression and RSSI rows because the
  primary behavior is polarity-controlled downconversion, not gain compression
  or power detection.

## Gate 2: Modeling And Evidence

- Status: `cadence_modeling_ready`.
- Prompt hygiene: public prompt now describes only the DUT contract, interface,
  observable behavior, and modeling boundary. Hidden-evaluator wording and
  repeated testbench-generation context were removed.
- Cadence/Verilog-A correspondence: the model uses event-updated state on
  `cross`, bounded voltage targets, and `transition()` smoothing for
  discontinuous target updates. This matches the local Cadence review guidance
  for transient behavioral Verilog-A macromodels while avoiding RF/PSS
  overclaiming.
- Visible/hidden coverage: visible smoke is a short compile/sim deck; hidden
  deck exercises positive and negative input-envelope deviations under both LO
  polarities. The starter file now drives benign constant voltage placeholders
  so the public smoke deck checks compile/transient packaging without passing
  hidden behavior.
- Checker strength: checker requires LO polarity to control conversion sign,
  verifies visible conversion gain, bounds baseband output, and rejects missing
  metric behavior.
- Negatives: 5/5 concrete variants reject behaviorally under EVAS.
- EVAS evidence: hidden gold PASS; concrete negatives 5/5 rejected with
  `FAIL_SIM_CORRECTNESS`.
- Spectre evidence: hidden gold PASS under the RF/AFE remaining review rerun.
- AHDL lint status: EVAS AHDL-like lint preflight PASS with zero diagnostics.

## Residual Risk

Spectre negatives were not rerun for every concrete negative variant in this
category closeout. The task is a transient voltage-domain RF/AFE macromodel and
should not be claimed as a Spectre RF/PSS-ready transistor-level RF model.
