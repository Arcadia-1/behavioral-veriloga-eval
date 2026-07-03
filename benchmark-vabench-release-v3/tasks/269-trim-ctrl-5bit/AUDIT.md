# Source Trim Ctrl 5bit Audit

- Source: `guoxy/ideal_TRIM_CTRL_5BITS.va` from the exact-deduplicated historical Verilog-A corpus.
- Gate 1: retained as the single scalar-to-trim-bits representative after manual review of `227-trim-ctrl-4bit`, `269-trim-ctrl-5bit`, and `296-cal4bit-modulo`. It has the strongest standalone behavior among the three because it combines nearest-integer conversion, explicit 5-bit clamp range, LSB-first output order, and clamp/offset/bit-order negative coverage.
- Scenario: scalar-to-5-bit calibration trim-control encoder. Round `ain` to the nearest integer, clamp to `0..31`, and drive `dout0..dout4` as voltage-coded LSB-first binary bits.
- Gate 2 repair: public prompt rewritten to remove source provenance and expose the observable trim-code contract. Gold now uses transition-smoothed voltage-coded outputs.
- 2026-07-03 validation: EVAS2 gold semantic validation passed and all five negatives were rejected. EVAS AHDL-like lint passed. Targeted Spectre AX gold semantic validation passed.
- AHDL lint/read-in triage: targeted Spectre logs contain no task-specific `AHDLLINT-*` findings or VACOMP errors. Remaining `VACOMP-2435` and `SPECTRE-592` messages are environment/setup warnings, not benchmark modeling failures.
- Import status: certified only after visible compile, EVAS/Spectre semantic validation, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
