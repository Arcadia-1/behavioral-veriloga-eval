# ADC Sample Clock Sequencer Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `adc_sample_clock_sequencer.va`: `adc_sample_clock_sequencer`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_PERIODIC_18NS_FRAME`: Generate a repeating 18 ns timing frame.
- `P_RESET_SAMPLE_AND_SS_WINDOWS`: `rst`, `s`, and `ss` are high only in the declared frame windows.
- `P_NONOVERLAP_AND_AUTOZERO_WINDOWS`: `nc` and `nc_az` use the declared non-overlap and autozero windows without swapping outputs.
- `P_CONVERSION_WINDOW_TIMING`: `conv` is asserted in the declared conversion windows with the correct phase.
- `P_TIMING_OUTPUT_LEVELS`: All timing outputs drive valid voltage-coded low/high levels.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `adc_sample_clock_sequencer.va`.
Every supplied `.va` file is editable; do not add or omit files.
