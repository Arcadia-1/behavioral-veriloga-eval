# Ideal Sample And Hold Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `source_sample_hold.va`: `source_sample_hold`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RISING_EDGE_CAPTURE`: On each rising vclk crossing through vtrans_clk, vout captures the instantaneous vin value.
- `P_INTEREDGE_HOLD`: The captured value holds until the next rising sampling event even when vin changes.
- `P_NO_FALLING_EDGE_CAPTURE`: Falling vclk crossings do not update the held value.
- `P_UNITY_SAMPLE_GAIN`: The held target equals the sampled vin without gain, offset, quantization, or rail remapping.
- `P_PARAMETERIZED_THRESHOLD`: Legal vtrans_clk overrides move the sampling crossing threshold while preserving rising-edge capture and hold behavior.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `source_sample_hold.va`.
Every supplied `.va` file is editable; do not add or omit files.
