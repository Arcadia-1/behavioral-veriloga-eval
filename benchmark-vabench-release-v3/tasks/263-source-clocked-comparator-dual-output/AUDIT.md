# Source Clocked Comparator Dual Output Audit

- Source: `caiyizeng25/comp_ideal.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a clocked comparator with complementary outputs. On each rising clock edge, latch VINP > VINN into OUTP/OUTN; on each falling clock edge, reset both outputs low after the comparator delay.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch28-evas/263-source-clocked-comparator-dual-output`
  - `WORK/source-import-batch28-spectre/263-source-clocked-comparator-dual-output`
