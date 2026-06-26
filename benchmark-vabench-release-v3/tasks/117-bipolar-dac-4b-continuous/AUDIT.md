# Audit: 117-bipolar-dac-4b-continuous

- Status: source import certified
- Source provenance: `shigao/DAC4bit_1.va`
- EVAS: PASS, checker `117-bipolar-dac-4b-continuous`
- Spectre: PASS, mode AX via SUI direct
- EVAS/Spectre parity: `passed`
- Spectre checker note: vout=-0.900,-0.300,0.300,0.900 monotonic=True
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
