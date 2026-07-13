# Sample Hold 5v Clock Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `sample_hold_5v_clock.va`: `sample_hold_5v_clock`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_DETECT_RISING_CROSSINGS_OF_VCLK_THROUGH`: Detect rising crossings of `vclk` through `vtrans_clk`. At each qualifying edge, sample the instantaneous value of `vin` and hold that sampled value on `vout` until the next rising clock edge. Falling clock edges must not update the held value.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `sample_hold_5v_clock.va`.
Every supplied `.va` file is editable; do not add or omit files.
