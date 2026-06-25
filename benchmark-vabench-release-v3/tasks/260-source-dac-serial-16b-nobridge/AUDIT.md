# Source DAC Serial 16b Nobridge Audit

- Source: `zhangz/DAC_serial_16b_nobridge_va.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement the serial SAR DAC accumulator. CLK_SAMPLE falling resets state and counter; each CLK_SARREADY falling edge consumes DATA and adds the next capacitor weight before driving a bipolar output.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch27-evas/260-source-dac-serial-16b-nobridge`
  - `WORK/source-import-batch27-spectre/260-source-dac-serial-16b-nobridge`
