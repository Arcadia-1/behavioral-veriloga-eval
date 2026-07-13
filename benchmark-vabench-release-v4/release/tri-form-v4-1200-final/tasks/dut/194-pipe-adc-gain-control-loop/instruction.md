# Pipe ADC Gain Control Loop

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `pipe_adc_gain_control_loop.va`: `pipe_adc_gain_control_loop`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_GAIN_CONTROL_INITIAL_STATE`: Initialize the gain-control code to `gaincodeinit` and initialize the test-DAC controls to the declared minus phase.
- `P_ALTERNATING_TEST_DAC_PHASES`: On rising `clks`, alternate minus and plus test-DAC phases using the sampled 7-bit input code.
- `P_TARGET_DIFFERENCE_GAIN_UPDATE`: Update the gain-control code from the plus/minus code difference using the declared target difference and correction polarity.
- `P_GAIN_OUTPUT_LEVELS`: Gain-control and test-DAC outputs use valid voltage-coded low/high levels.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `pipe_adc_gain_control_loop.va`.
Do not add or omit artifacts.
