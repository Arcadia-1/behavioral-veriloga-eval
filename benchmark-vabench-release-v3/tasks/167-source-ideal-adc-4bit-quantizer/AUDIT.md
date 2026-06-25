# Source Ideal ADC 4bit Quantizer Audit

- Source: `zhaoh/IDEAL_ADC.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: rising-edge sampled differential ADC quantization.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch10-evas/167-source-ideal-adc-4bit-quantizer`
  - `WORK/source-import-batch10-spectre/167-source-ideal-adc-4bit-quantizer`
