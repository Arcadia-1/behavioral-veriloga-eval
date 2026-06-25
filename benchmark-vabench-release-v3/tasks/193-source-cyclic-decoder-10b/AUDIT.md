# Source Cyclic Decoder 10b Audit

- Source: `zhangm/cyclic_decoder.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: ready-pulsed cyclic ADC decision accumulation and normalized output.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch14-evas/193-source-cyclic-decoder-10b`
  - `WORK/source-import-batch14-spectre/193-source-cyclic-decoder-10b`
