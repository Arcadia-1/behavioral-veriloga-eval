# Source SPI Shift Mux Audit

- Source: `zhangz/L3_SPI_MUX_Big_V1.va` from the exact-deduplicated historical Verilog-A corpus.
- Gate 1: retained as a support/control L1 utility for AMS configuration paths, not a core analog block. It is distinct from the wider generic `config_shift_reg_64b` support row because this task exposes an 8-bit mux-control word, SDO, forwarded SCK, and reset reload behavior.
- Scenario: serially shifted mux configuration word with active-high reset reload, SDO, and forwarded SCK.
- Gate 2 repair: reset is now a public behavior contract rather than an unused interface pin. The gold, visible/hidden stimulus, checker, and a concrete negative all exercise active-high reset reload to the initial word `10110010`.
- 2026-07-03 validation: EVAS2 gold semantic validation passed and all five negatives were rejected. EVAS AHDL-like lint passed after changing `scko` to use an event-updated discrete clock state before `transition()`. Targeted Spectre AX gold semantic validation passed.
- AHDL lint/read-in triage: targeted Spectre logs contain no task-specific `AHDLLINT-*` findings or VACOMP errors. Remaining `VACOMP-2435` and `SPECTRE-592` messages are environment/setup warnings, not benchmark modeling failures.
- Import status: certified only after visible compile, EVAS/Spectre semantic validation, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
