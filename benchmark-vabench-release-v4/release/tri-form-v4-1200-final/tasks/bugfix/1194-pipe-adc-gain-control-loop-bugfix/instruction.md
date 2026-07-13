# Pipe ADC Gain Control Loop Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `pipe_adc_gain_control_loop.va`: `pipe_adc_gain_control_loop`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_GAIN_CONTROL_INITIAL_STATE`: Initialize the gain-control code to `gaincodeinit` and initialize the test-DAC controls to the declared minus phase.
- `P_ALTERNATING_TEST_DAC_PHASES`: On rising `clks`, alternate minus and plus test-DAC phases using the sampled 7-bit input code.
- `P_TARGET_DIFFERENCE_GAIN_UPDATE`: Update the gain-control code from the plus/minus code difference using the declared target difference and correction polarity.
- `P_GAIN_OUTPUT_LEVELS`: Gain-control and test-DAC outputs use valid voltage-coded low/high levels.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `pipe_adc_gain_control_loop.va`.
Every supplied `.va` file is editable; do not add or omit files.
