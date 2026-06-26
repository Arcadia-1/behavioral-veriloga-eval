# Source Coarse QTZ 3bit Residue Audit

- Source: `liukezhuo/coarse_QTZ3bit.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a clipped 3-bit coarse quantizer over -VREF..+VREF. Drive binary code bits and the analog residue VIN - Vquantized.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch29-evas/271-coarse-qtz-3bit-residue`
  - `WORK/source-import-batch29-spectre/271-coarse-qtz-3bit-residue`
