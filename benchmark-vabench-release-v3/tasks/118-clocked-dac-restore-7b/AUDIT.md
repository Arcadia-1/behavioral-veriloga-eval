# Audit: 118-clocked-dac-restore-7b

- Status: source import certified
- Source provenance: `wangxy/DAC_restore_7bit.va`
- EVAS: PASS, checker `118-clocked-dac-restore-7b`
- Spectre: PASS, mode AX via SUI direct
- EVAS/Spectre parity: `passed`
- Spectre checker note: vout=-0.893,-0.302,0.302,0.893 monotonic=True
- Evidence:
  - `WORK/source-import-batch2-evas/summary.json`
  - `WORK/source-import-batch2-spectre/summary.json`

## Four-Standard Review

- Useful scenario: yes. This is a reusable source-derived voltage-domain primitive for converter, timing, or logic behavioral flows.
- Reasonable task: yes. The public task is a single DUT with fixed port order and bounded scope.
- Complete tests: yes for this import stage. Visible smoke compiles starter; hidden gold runs EVAS and Spectre on the same testbench with semantic checker.
- Fair evaluation: yes. The checker samples stable windows after events and does not require raw timestep equality.

## Submit Decision

Can submit: yes. This task passed visible smoke, EVAS hidden gold, Spectre AX hidden gold, and EVAS/Spectre parity.
