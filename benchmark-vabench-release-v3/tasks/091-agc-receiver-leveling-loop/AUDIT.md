# Two-Gate Audit: Task 091 AGC Receiver Leveling Loop

## Gate 1: Admission

- Label: `l2_core_ready`.
- Human-review status: proposed for retention as an RF/AFE receiver-control L2
  row.
- Function boundary: a composed AGC receiver macromodel combining receiver gain
  path, output-envelope/RSSI observation, gain-control update, bounded output,
  and lock/target metric.
- Duplicate check: distinct from simple gain/limiter rows because the behavior
  is closed-loop gain reduction and settling toward a target amplitude, not a
  static gain or compression transfer curve.

## Gate 2: Modeling And Evidence

- Status: `cadence_modeling_ready`.
- Prompt hygiene: public prompt now states the DUT interface and observable AGC
  behavior directly. Migration history, hidden-evaluator wording, and
  testbench-generation text were removed.
- Cadence/Verilog-A correspondence: the model uses event-updated state on the
  gain-control clock, explicit reset initialization, bounded monitor variables,
  and `transition()` smoothing for output contributions. Stored state is
  documented as transient behavioral state, not a Spectre RF/PSS claim.
- Visible/hidden coverage: hidden stimulus now differs from visible by reset
  release timing and input-envelope levels while still exercising low-input,
  overload, and settled-gain windows.
- Checker strength: checker requires small-signal amplification, overload
  response, gain-monitor reduction, RSSI overload sensitivity, settled output
  amplitude, and metric assertion near target.
- Negatives: 5/5 concrete variants reject behaviorally under EVAS.
- EVAS evidence: hidden gold PASS; concrete negatives 5/5 rejected with
  `FAIL_SIM_CORRECTNESS`.
- Spectre evidence: hidden gold PASS under the RF/AFE remaining review rerun.
- AHDL lint status: EVAS AHDL-like lint preflight PASS with zero diagnostics.

## Residual Risk

Spectre negatives were not rerun for every concrete negative variant in this
category closeout. The row is a transient voltage-domain behavioral receiver
subsystem, not a transistor-level AGC implementation or RF/PSS-ready model.
