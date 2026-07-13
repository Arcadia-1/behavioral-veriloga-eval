# CTLE Adaptation Loop Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `ctle_adaptation_loop_top.va`: `ctle_adaptation_loop_top`
- `ctle_boost_core.va`: `ctle_boost_core`
- `boost_adapt_controller.va`: `boost_adapt_controller`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear boost code, output, metric, and `locked`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, compare `edge_metric_in` with `edge_target`.
- `P_INCREASE_BOOST_CODE_WHEN_EDGE_METRIC`: Increase boost code when edge metric is too low and decrease it when too high.
- `P_DRIVE_VOUT_AS_A_BOOSTED_VERSION`: Drive `vout` as a boosted version of `vin - vcm` using the active boost code.
- `P_ASSERT_LOCKED_AFTER_THREE_CONSECUTIVE_UPDATES`: Assert `locked` after three consecutive updates within the target tolerance.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `ctle_adaptation_loop_top.va`, `ctle_boost_core.va`, `boost_adapt_controller.va`.
Every supplied `.va` file is editable; do not add or omit files.
