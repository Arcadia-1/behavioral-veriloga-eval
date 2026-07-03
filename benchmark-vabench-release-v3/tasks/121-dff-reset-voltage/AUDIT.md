# Audit: 121-dff-reset-voltage

- Status: source import certified
- EVAS: PASS, checker `121-dff-reset-voltage`
- Spectre: PASS, mode AX via SUI direct
- EVAS/Spectre parity: `passed`
- Spectre checker note: vout_q=0.900,0.000,0.900,0.000,0.900 vout_qbar=0.000,0.900,0.000,0.000,0.000

## Four-Standard Review

- Useful scenario: yes. This is a reusable source-derived voltage-domain primitive for converter, timing, or logic behavioral flows.
- Reasonable task: yes. The public task is a single DUT with fixed port order and bounded scope.
- Complete tests: yes for this import stage. Visible smoke compiles starter; gold semantic validation runs EVAS and Spectre on the same testbench with semantic checker.
- Fair evaluation: yes. The checker samples stable windows after events and does not require raw timestep equality.

## Submit Decision

Can submit: yes. This task passed visible smoke, EVAS/Spectre gold semantic validation, and EVAS/Spectre parity.

## Digital/Control/Logic Closeout Review

- Gate 1 status: `l2_support_component`.
- Rationale: resettable voltage-coded DFF behavior is useful for converter,
  timing, and control flows, but it is a generic state primitive as written.
- Counting recommendation: do not count as core analog/mixed-signal function
  unless the benchmark policy explicitly includes digital-control primitives.
