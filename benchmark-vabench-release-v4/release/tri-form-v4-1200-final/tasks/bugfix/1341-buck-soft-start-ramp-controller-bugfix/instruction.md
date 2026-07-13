# Buck Soft-start Ramp Controller Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `buck_soft_start_ramp_controller.va`: `buck_soft_start_ramp_controller`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear `soft_ref`, ramp metric, and `done`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, increase `soft_ref` toward `target_ref` by at most `ramp_step`.
- `P_NEVER_ALLOW_SOFT_REF_TO_EXCEED`: Never allow `soft_ref` to exceed `target_ref` or the public rails.
- `P_EXPOSE_THE_REMAINING_RAMP_DISTANCE_ON`: Expose the remaining ramp distance on `ramp_metric`.
- `P_ASSERT_DONE_ONLY_AFTER_SOFT_REF`: Assert `done` only after `soft_ref` reaches the target within `ramp_tol`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `buck_soft_start_ramp_controller.va`.
Every supplied `.va` file is editable; do not add or omit files.
