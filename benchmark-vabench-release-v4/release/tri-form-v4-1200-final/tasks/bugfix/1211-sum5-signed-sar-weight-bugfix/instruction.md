# SUM5 Signed SAR Weight Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `sum5_signed_sar_weight.va`: `sum5_signed_sar_weight`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_TREAT_EACH_DECISION_INPUT_AS_1`: Treat each decision input as `+1` when its voltage is above `vth` and `-1` otherwise. Combine the signed decisions with SAR weights `d5 = 1/2`, `d4 = 1/4`, `d3 = 1/8`, `d2 = 1/16`, and `d1 = 1/32`. Drive `out` to the scaled signed reconstruction:
- `P_TEXT_OUT_1_1_2_SIGNED`: ```text out = 1.1 * (2 * signed_weighted_sum - 1) ```
- `P_THE_BEHAVIOR_IS_CONTINUOUS_WITH_RESPECT`: The behavior is continuous with respect to the voltage-coded decision inputs after thresholding.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `sum5_signed_sar_weight.va`.
Every supplied `.va` file is editable; do not add or omit files.
