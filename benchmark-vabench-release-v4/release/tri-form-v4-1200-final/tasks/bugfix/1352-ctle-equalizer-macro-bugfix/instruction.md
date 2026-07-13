# CTLE Equalizer Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `ctle_equalizer.va`: `ctle_equalizer`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_INITIALIZES_THE_EQUALIZED_OUTPUT_TO`: Reset initializes the equalized output to common mode and clears metric outputs.
- `P_ON_EACH_RISING_CLK_SAMPLE_THE`: On each rising `clk`, sample the boost code and the current input.
- `P_DRIVE_VOUT_FROM_THE_CURRENT_INPUT`: Drive `vout` from the current input plus a boost-code-scaled edge term relative to the previous sampled input.
- `P_CLAMP_VOUT_TO_THE_VSS_TO`: Clamp `vout` to the `vss` to `vdd` range.
- `P_EDGE_METRIC_REPORTS_THE_ABSOLUTE_BOOSTED`: `edge_metric` reports the absolute boosted edge contribution after clipping to full scale.
- `P_SAT_FLAG_IS_HIGH_WHEN_THE`: `sat_flag` is high when the unclamped equalized target would exceed either output rail.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `ctle_equalizer.va`.
Every supplied `.va` file is editable; do not add or omit files.
