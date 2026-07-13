# Clocked Four Input Mux Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `clocked_four_input_mux.va`: `clocked_four_input_mux`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_FALLING_EDGE_SAMPLE_HOLD`: Only falling `clks` crossings through `vth` update `dout`; between those events the last selected input value is held.
- `P_SELECT_BIT_DECODE`: `dsel0` is the LSB and `dsel1` is the MSB when selecting among `din0` through `din3`.
- `P_ALL_FOUR_INPUTS_REACHABLE`: All four data inputs can be selected and forwarded to `dout` according to the two-bit select code.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `clocked_four_input_mux.va`.
Every supplied `.va` file is editable; do not add or omit files.
