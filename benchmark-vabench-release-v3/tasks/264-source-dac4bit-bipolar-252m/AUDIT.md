# Source DAC4bit Bipolar 252m Audit

- Source: `chengqidong25/DAC4bit.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a continuous 4-bit binary DAC. Bits d3..d0 encode 0..15 and drive vout = vref * (2*code/15 - 1) with the source model's 252 mV full-scale reference.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch28-evas/264-source-dac4bit-bipolar-252m`
  - `WORK/source-import-batch28-spectre/264-source-dac4bit-bipolar-252m`
