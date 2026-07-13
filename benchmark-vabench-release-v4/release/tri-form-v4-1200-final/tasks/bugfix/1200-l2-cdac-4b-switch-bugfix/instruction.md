# L2 CDAC 4b Switch Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `l2_cdac_4b_switch.va`: `l2_cdac_4b_switch`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_FIRST_READY_EDGE_ARMS_ONLY`: The first rising `rdy` edge arms the DAC and leaves the initialized output at zero.
- `P_READY_SAMPLES_FOUR_BITS`: Each later rising `rdy` edge samples `din1..din4` against `vth` with the declared switched weights.
- `P_SWITCHED_WEIGHT_DENOMINATOR`: Compute `switched_weight` and normalize by `8.5` before output scaling.
- `P_BIPOLAR_CDAC_OUTPUT`: Map the sampled ratio to `(switched_weight / 8.5) * 2.0 * vdd - vdd` and hold it between ready edges.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `l2_cdac_4b_switch.va`.
Every supplied `.va` file is editable; do not add or omit files.
