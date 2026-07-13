# Baseband Anti-alias Filter Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `baseband_antialias_filter_macro.va`: `baseband_antialias_filter_macro`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` to `vcm`, clear metric, and clear `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, decode `bw_1..bw_0` as a bandwidth setting.
- `P_UPDATE_VOUT_AS_A_FIRST_ORDER`: Update `vout` as a first-order discrete-time low-pass response to `vin`.
- `P_HIGHER_BANDWIDTH_CODE_MUST_MOVE_VOUT`: Higher bandwidth code must move `vout` closer to `vin` per update.
- `P_EXPOSE_THE_ACTIVE_BANDWIDTH_CODE_ON`: Expose the active bandwidth code on `bandwidth_metric` and assert `valid` after the first update.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `baseband_antialias_filter_macro.va`.
Every supplied `.va` file is editable; do not add or omit files.
