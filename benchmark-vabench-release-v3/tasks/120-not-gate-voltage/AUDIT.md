# Audit: 120-not-gate-voltage

- Status: source import certified
- Source provenance: `wangx/not_gate.va`
- EVAS: PASS, checker `120-not-gate-voltage`
- Spectre: PASS, mode AX via SUI direct
- EVAS/Spectre parity: `passed`
- Spectre checker note: vout=0.900,0.000,0.900,0.000,0.900
## Four-Standard Review

- Useful scenario: yes. This is a reusable source-derived voltage-domain primitive for converter, timing, or logic behavioral flows.
- Reasonable task: yes. The public task is a single DUT with fixed port order and bounded scope.
- Complete tests: yes for this import stage. Visible smoke compiles starter; gold semantic validation runs EVAS and Spectre on the same testbench with semantic checker.
- Fair evaluation: yes. The checker samples stable windows after events and does not require raw timestep equality.

## Submit Decision

Can submit: yes. This task passed visible smoke, EVAS/Spectre gold semantic validation, and EVAS/Spectre parity.

## Gate 1 Counting Review

- Status: `l2_support_component` / support-regression candidate, not a strong core scored benchmark as written.
- Rationale: the task is a small thresholded Boolean primitive with rail-coded output. It is useful inside AMS control, converter, sampler, or calibration flows, but it does not by itself expose a distinct analog/mixed-signal function boundary.
- Counting recommendation: keep as a support utility or L0-style regression row; do not count as an independent core circuit benchmark unless rewritten into a larger AMS decision/control role.
