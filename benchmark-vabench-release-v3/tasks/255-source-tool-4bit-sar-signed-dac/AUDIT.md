# Source Tool 4bit SAR Signed DAC Audit

- Source: `liaoyuhui/_tool_4bit_sar.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a sample-triggered signed 4-bit SAR helper DAC. On SH rising, each bit contributes +weight if high and -weight if low, with weights 8, 4, 2, 1 and gain 1.8/16.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch26-evas/255-source-tool-4bit-sar-signed-dac`
  - `WORK/source-import-batch26-spectre/255-source-tool-4bit-sar-signed-dac`
