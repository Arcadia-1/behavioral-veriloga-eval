# VGA Step-response Classifier Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `vga_step_response_classifier.va`: `vga_step_response_classifier`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` to `vcm`, clear metric, and clear `settled`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, decode the gain code and update the target output from `vin`.
- `P_APPLY_BOUNDED_SETTLING_WITH_A_CODE`: Apply bounded settling with a code-dependent overshoot proxy after large gain changes.
- `P_EXPOSE_OVERSHOOT_MAGNITUDE_ON_OVERSHOOT_METRIC`: Expose overshoot magnitude on `overshoot_metric`.
- `P_ASSERT_SETTLED_AFTER_TWO_CONSECUTIVE_UPDATES`: Assert `settled` after two consecutive updates within `settle_tol` of the target.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `vga_step_response_classifier.va`.
Every supplied `.va` file is editable; do not add or omit files.
