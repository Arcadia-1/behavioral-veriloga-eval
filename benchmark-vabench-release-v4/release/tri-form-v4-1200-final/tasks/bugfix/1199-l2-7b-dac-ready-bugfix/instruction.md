# L2 7b DAC Ready Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `l2_7b_dac_ready.va`: `l2_7b_dac_ready`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_FIRST_READY_EDGE_ARMS_ONLY`: The first rising `rdy` edge arms the DAC and leaves the initialized output at zero.
- `P_READY_SAMPLES_SEVEN_BITS`: Each later rising `rdy` edge samples `din1..din7` against `vth` with the declared switched-capacitor weights.
- `P_BIPOLAR_WEIGHTED_DAC_OUTPUT`: Map the sampled 7-bit weight to the declared bipolar single-ended output with the correct denominator and offset.
- `P_DAC_OUTPUT_LEVEL_AND_HOLD`: Hold `aout` between ready edges and drive the declared voltage scale without half-level errors.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `l2_7b_dac_ready.va`.
Every supplied `.va` file is editable; do not add or omit files.
