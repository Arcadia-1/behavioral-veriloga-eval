# FFE Tap Adaptation Monitor Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `ffe_tap_adaptation_monitor_top.va`: `ffe_tap_adaptation_monitor_top`
- `tap_update_controller.va`: `tap_update_controller`
- `cursor_metric_core.va`: `cursor_metric_core`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear tap states, output, adapt metric, and `done`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, update pre and post tap signs according to `err_in - vcm`.
- `P_DRIVE_MAIN_OUT_AS_THE_CURRENT`: Drive `main_out` as the current main cursor correction around `vcm`.
- `P_EXPOSE_AGGREGATE_TAP_MAGNITUDE_ON_ADAPT`: Expose aggregate tap magnitude on `adapt_metric`.
- `P_ASSERT_DONE_AFTER_SIX_ENABLED_ADAPTATION`: Assert `done` after six enabled adaptation updates.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `ffe_tap_adaptation_monitor_top.va`, `tap_update_controller.va`, `cursor_metric_core.va`.
Every supplied `.va` file is editable; do not add or omit files.
