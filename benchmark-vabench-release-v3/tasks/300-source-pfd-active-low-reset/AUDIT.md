# Source PFD Active Low Reset Audit

- Source: `taoy/v_PFD.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a PFD with active-low UPB and active-high DOWN. A rising REF asserts UPB low; a rising FB asserts DOWN high; both reset after both edges arrive.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch32-evas/300-source-pfd-active-low-reset`
  - `WORK/source-import-batch32-spectre/300-source-pfd-active-low-reset`
