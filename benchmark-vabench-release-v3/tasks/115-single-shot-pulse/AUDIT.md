# Audit: 115-single-shot-pulse

- Status: source import certified
- Source provenance: `wangx/single_shot.va`
- EVAS: PASS, checker `115-single-shot-pulse`
- Spectre: PASS, mode AX via SUI direct
- EVAS/Spectre parity: `passed`
- Spectre checker note: vout=0.000,0.900,0.900,0.000,0.000,0.900,0.900,0.000 high_windows=[8.0, 14.0, 28.0, 34.0] low_windows=[4.0, 18.0, 24.0, 38.0]
- Evidence: historical local source-import report paths are omitted from the public package; rerun current validation scripts for fresh evidence.

## Four-Standard Review

- Useful scenario: yes. This is a reusable source-derived voltage-domain primitive for converter/timing behavioral flows.
- Reasonable task: yes. The public task is a single DUT with fixed port order and bounded scope.
- Complete tests: yes for this import stage. Visible smoke compiles starter; hidden gold runs EVAS and Spectre on the same testbench with semantic checker.
- Fair evaluation: yes. The checker samples stable windows after events and does not require raw timestep equality.

## Submit Decision

Can submit: yes. This task passed visible smoke, EVAS hidden gold, Spectre AX hidden gold, and EVAS/Spectre parity.
