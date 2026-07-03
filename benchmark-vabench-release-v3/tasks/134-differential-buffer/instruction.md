# Differential Buffer

## Task Contract
Implement the Verilog-A support module `differential_buffer.va` for a unity-gain differential pass-through buffer.

## Form-Specific Requirements
This is a small support/component task. The solver should implement the stated interface behavior without adding gain, delay, common-mode conversion, or rail logic.

## Public Verilog-A Interface
Provide `module differential_buffer(VINP, VINN, VOUTP, VOUTN);` with electrical inputs `VINP`, `VINN` and electrical outputs `VOUTP`, `VOUTN`.

## Public Parameter Contract
This task has no public parameters.

## Required Behavior
Drive `VOUTP` from `VINP` and `VOUTN` from `VINN` with unity gain and the same polarity on each side.

## Modeling Constraints
Use direct voltage contributions. Do not swap polarity, collapse the output to common mode, or add hidden state.

## Output Contract
Submit only the completed Verilog-A module in `differential_buffer.va`.
