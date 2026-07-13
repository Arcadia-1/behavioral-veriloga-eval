# Programmable Gain Amplifier Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `programmable_gain_amplifier.va`: `programmable_gain_amplifier`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_UNITY`: While rst is active, the sampled gain is unity, out is vcm, and metric is low.
- `P_SAMPLED_GAIN_SELECT`: Each rising clk crossing with reset inactive samples gain_sel, selecting gain_high above vth and gain_low below vth; the selection holds between crossings.
- `P_COMMON_MODE_GAIN`: The unclamped output target is vcm plus the sampled gain times vin minus vcm.
- `P_OUTPUT_CLAMP`: Out is limited to the inclusive vmin through vmax range with finite smoothing.
- `P_CLIP_METRIC`: Metric is high exactly when the unclamped target lies outside vmin through vmax, and low otherwise; reset forces it low.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `programmable_gain_amplifier.va`.
Every supplied `.va` file is editable; do not add or omit files.
