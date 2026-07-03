# Source Trim Ctrl 4bit Audit

- Gate 1: duplicate/support after manual trim-code review. Do not count separately together with `269-trim-ctrl-5bit`; both are scalar analog-code to voltage-coded trim-bit encoders, and the width difference alone is not enough for an independent benchmark function.
- Current disposition: keep as historical/support material unless upstream chooses this row instead of `269`; the retained representative in this review is `269-trim-ctrl-5bit` because it includes an explicit 5-bit clamp range and stronger negative coverage.
- Scenario: analog trim-code decoder that converts an input code voltage into four binary trim control rails.
- Import status: certified only after visible compile, EVAS/Spectre semantic validation, and EVAS/Spectre parity pass.
- Evaluation: stable sampled behavior from `tran.csv`; raw simulator timestep equality is not used.
