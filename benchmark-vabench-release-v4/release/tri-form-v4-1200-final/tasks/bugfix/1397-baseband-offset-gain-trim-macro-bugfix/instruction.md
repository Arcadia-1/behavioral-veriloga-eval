# Baseband Offset-and-gain Trim Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `baseband_offset_gain_trim_macro.va`: `baseband_offset_gain_trim_macro`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_OR_LOW_ENABLE_DRIVES_VOUT`: Reset or low `enable` drives `vout` to common mode, clears residual metric, and clears `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_SAMPLE`: On each enabled rising `clk`, sample gain and offset trim codes.
- `P_USE_GAIN_GAIN_BASE_GAIN_STEP`: Use `gain = gain_base + gain_step * gain_code`.
- `P_USE_SIGNED_OFFSET_OFFSET_CODE_3`: Use signed offset `(offset_code - 3) * offset_lsb`.
- `P_DRIVE_VOUT_AS_THE_CLIPPED_GAIN`: Drive `vout` as the clipped gain-and-offset adjusted input around common mode.
- `P_RESIDUAL_METRIC_REPORTS_THE_ABSOLUTE_OUTPUT`: `residual_metric` reports the absolute output distance from common mode and `valid` marks that a trim sample has occurred.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `baseband_offset_gain_trim_macro.va`.
Every supplied `.va` file is editable; do not add or omit files.
