# Source CAL4bit Modulo Audit

- Gate 1: duplicate/support after manual trim-code review. Do not count separately together with `227-trim-ctrl-4bit` and `269-trim-ctrl-5bit`; as written, the independent behavior is only scalar analog-code to binary trim rails with a different width/rounding policy.
- Current disposition: keep as historical/support material unless upstream wants the floor-then-clamp policy as the representative. This review retains `269-trim-ctrl-5bit` as the stronger trim-code benchmark.
- Naming note: despite the historical task/module name, the behavior is floor-then-clamp encoding, not modulo wrapping.
- Scenario: scalar-to-4-bit calibration encoder. Floor the input voltage to an integer code, clamp to `0..15`, and emit four voltage-coded bits.
- Import status: certified only after visible compile, EVAS/Spectre semantic validation, EVAS/Spectre parity pass, and negative variant rejection.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.

## Window B Calibration Closeout

- Gate 2 status: `duplicate_support_not_counted`.
- Evidence: Window B targeted review on 2026-07-03 recorded EVAS hidden gold PASS, 5/5 concrete negatives rejected, AHDL-like lint PASS with 0 diagnostics, and targeted Spectre hidden gold PASS.
- Gold cleanup: output bits were smoothed with `transition(...)`.
- Counting recommendation: keep as valid support/historical material only. Do not count separately with retained `269-trim-ctrl-5bit` and `227-trim-ctrl-4bit`; the behavior remains scalar code-to-trim rails with floor/clamp policy.
