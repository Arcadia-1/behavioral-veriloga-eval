# Source Folded Flash DAC 4b Audit

- Source: `zhangad/dac_4bit_flash_ideal.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: folded 4-bit flash DAC code-to-voltage reconstruction.
- Note: the imported solution uses an event-updated equivalent of the source
  threshold comparisons so EVAS and Spectre sample the same stable DAC code.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch13-evas/186-folded-flash-dac-4b`
  - `WORK/source-import-batch13-spectre/186-folded-flash-dac-4b`
