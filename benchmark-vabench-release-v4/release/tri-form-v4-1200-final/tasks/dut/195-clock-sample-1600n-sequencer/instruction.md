# Clock Sample 1600n Sequencer

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `clock_sample_1600n_sequencer.va`: `clock_sample_1600n_sequencer`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_PERIODIC_16NS_FRAME`: Generate a repeating 16 ns ADC timing frame.
- `P_RESET_AND_SAMPLE_WINDOWS`: `rst` and `s` are high only in the declared frame windows, including both sample windows.
- `P_NONOVERLAP_AND_RESIDUE_WINDOWS`: `nc` and `res` use the declared non-overlap and residue windows without swapping outputs.
- `P_CONVERSION_OUTPUT_TIMING`: `conv` is asserted in the declared conversion windows with valid timing and level.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `clock_sample_1600n_sequencer.va`.
Do not add or omit artifacts.
