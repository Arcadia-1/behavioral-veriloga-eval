# ADC Sample Clock Sequencer

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `adc_sample_clock_sequencer.va`: `adc_sample_clock_sequencer`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_PERIODIC_18NS_FRAME`: Generate a repeating 18 ns timing frame.
- `P_RESET_SAMPLE_AND_SS_WINDOWS`: `rst`, `s`, and `ss` are high only in the declared frame windows.
- `P_NONOVERLAP_AND_AUTOZERO_WINDOWS`: `nc` and `nc_az` use the declared non-overlap and autozero windows without swapping outputs.
- `P_CONVERSION_WINDOW_TIMING`: `conv` is asserted in the declared conversion windows with the correct phase.
- `P_TIMING_OUTPUT_LEVELS`: All timing outputs drive valid voltage-coded low/high levels.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `adc_sample_clock_sequencer.va`.
Do not add or omit artifacts.
