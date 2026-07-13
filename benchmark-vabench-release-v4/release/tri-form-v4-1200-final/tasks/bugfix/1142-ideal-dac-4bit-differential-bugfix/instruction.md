# Ideal DAC 4bit Differential Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `ideal_dac_4bit_differential.va`: `ideal_dac_4bit_differential`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_FALLING_EDGE_CODE_SAMPLE`: Each falling `clk` crossing through `vtrans_clk` samples `digital`, clamps it to the valid code range, and holds the converted output until the next sample.
- `P_MIDRISE_DIFFERENTIAL_SCALE`: The sampled code maps to a mid-rise differential DAC level with the declared `levels` and `vref` scale.
- `P_OUTPUT_POLARITY_AND_COMMON_MODE`: `vop` and `von` are complementary about `vcm`, with positive differential polarity for larger sampled codes.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `ideal_dac_4bit_differential.va`.
Every supplied `.va` file is editable; do not add or omit files.
