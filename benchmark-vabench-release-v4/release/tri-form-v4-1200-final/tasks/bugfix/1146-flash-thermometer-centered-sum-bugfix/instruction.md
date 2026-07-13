# Flash Thermometer Centered Sum Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `flash_thermometer_centered_sum.va`: `flash_thermometer_centered_sum`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_THERMOMETER_THRESHOLD_COUNT`: Each `b0` through `b7` input above `vth` contributes exactly one count to the thermometer total.
- `P_CENTERED_SUM`: The output subtracts the four-count midpoint so the analog sum is centered around zero asserted-input balance.
- `P_OUTPUT_GAIN`: The centered count is multiplied by `gain` and driven on `dout` without extra scaling.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `flash_thermometer_centered_sum.va`.
Every supplied `.va` file is editable; do not add or omit files.
