# Clock Sample 1600n Sequencer Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `clock_sample_1600n_sequencer.va`: `clock_sample_1600n_sequencer`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_PERIODIC_16NS_FRAME`: Generate a repeating 16 ns ADC timing frame.
- `P_RESET_AND_SAMPLE_WINDOWS`: `rst` and `s` are high only in the declared frame windows, including both sample windows.
- `P_NONOVERLAP_AND_RESIDUE_WINDOWS`: `nc` and `res` use the declared non-overlap and residue windows without swapping outputs.
- `P_CONVERSION_OUTPUT_TIMING`: `conv` is asserted in the declared conversion windows with valid timing and level.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `clock_sample_1600n_sequencer.va`.
Every supplied `.va` file is editable; do not add or omit files.
