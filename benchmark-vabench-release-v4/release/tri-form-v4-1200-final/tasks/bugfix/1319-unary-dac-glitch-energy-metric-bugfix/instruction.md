# Unary DAC Glitch-energy Metric Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `unary_dac_glitch_energy_metric.va`: `unary_dac_glitch_energy_metric`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear output, previous code, glitch metric, and `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, decode the 3-bit code as a unary element count.
- `P_DRIVE_VOUT_PROPORTIONAL_TO_THE_DECODED`: Drive `vout` proportional to the decoded count.
- `P_DRIVE_GLITCH_METRIC_PROPORTIONAL_TO_THE`: Drive `glitch_metric` proportional to the absolute change in count since the previous enabled update.
- `P_ASSERT_VALID_AFTER_THE_FIRST_ENABLED`: Assert `valid` after the first enabled code update.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `unary_dac_glitch_energy_metric.va`.
Every supplied `.va` file is editable; do not add or omit files.
