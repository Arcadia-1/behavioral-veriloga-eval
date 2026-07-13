# Glitchless Clock Mux Selector Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `glitchless_clock_mux_selector.va`: `glitchless_clock_mux_selector`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `clk_out`, `switch_metric`, and `valid` low.
- `P_ROUTE_CLK_A_WHEN_SEL_IS`: Route `clk_a` when `sel` is low and `clk_b` when `sel` is high.
- `P_WHEN_SEL_CHANGES_WAIT_UNTIL_BOTH`: When `sel` changes, wait until both input clocks are low before changing the active source.
- `P_EXPOSE_A_SWITCH_EVENT_ON_SWITCH`: Expose a switch event on `switch_metric` for one output cycle after the selected source changes.
- `P_ASSERT_VALID_AFTER_THE_SELECTED_SOURCE`: Assert `valid` after the selected source has produced one clean output edge.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `glitchless_clock_mux_selector.va`.
Every supplied `.va` file is editable; do not add or omit files.
