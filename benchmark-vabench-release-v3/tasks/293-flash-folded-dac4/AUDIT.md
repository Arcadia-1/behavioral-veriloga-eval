# Source Flash Folded DAC4 Audit

- Source: `zhangad/dac_4bit_flash_ideal.va` from the exact-deduplicated historical Verilog-A corpus.
- Scenario: Implement a 4-input folded flash DAC. The MSB both contributes weight 8 and selects whether the output uses code or 8-code.
- Import status: certified only after visible compile, EVAS hidden semantic check, Spectre AX hidden semantic check, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
- Evidence:
  - `WORK/source-import-batch32-evas/293-flash-folded-dac4`
  - `WORK/source-import-batch32-spectre/293-flash-folded-dac4`
