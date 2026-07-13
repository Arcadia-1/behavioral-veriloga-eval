# PAM4 Linearity Monitor Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `pam4_linearity_monitor.va`: `pam4_linearity_monitor`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear output, metric, and `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, decode `symbol_1..symbol_0` as one of four PAM4 levels.
- `P_DRIVE_LEVEL_OUT_TO_EVENLY_SPACED`: Drive `level_out` to evenly spaced voltage levels between `vss` and `vdd`.
- `P_EXPOSE_A_LINEARITY_METRIC_THAT_IS`: Expose a `linearity_metric` that is high only when adjacent level spacing is uniform.
- `P_ASSERT_VALID_AFTER_EACH_SAMPLED_SYMBOL`: Assert `valid` after each sampled symbol update.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `pam4_linearity_monitor.va`.
Every supplied `.va` file is editable; do not add or omit files.
