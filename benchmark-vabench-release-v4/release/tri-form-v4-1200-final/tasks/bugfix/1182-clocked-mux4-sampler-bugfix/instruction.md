# Clocked Mux4 Sampler Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `clocked_mux4_sampler.va`: `clocked_mux4_sampler`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_SELECTS_DIN0`: While `rst` is high, the selected channel and `dout` are forced to `din0`.
- `P_FALLING_CLOCK_UPDATE_SAMPLE`: On each falling `clks` crossing with reset inactive and `update` high, latch `dsel0/dsel1` and sample the selected input.
- `P_UPDATE_LOW_HOLDS_STATE`: On falling `clks` crossings with `update` low, hold the previous selection and output value.
- `P_SELECT_DECODE_AND_OUTPUT_TIMING`: The held two-bit selection maps to `din0..din3` in binary order and drives `dout` with the declared transition timing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `clocked_mux4_sampler.va`.
Every supplied `.va` file is editable; do not add or omit files.
