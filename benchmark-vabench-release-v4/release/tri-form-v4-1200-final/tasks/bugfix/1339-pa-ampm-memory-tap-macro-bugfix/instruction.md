# PA AM/PM Memory Tap Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `pa_ampm_memory_tap_macro.va`: `pa_ampm_memory_tap_macro`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` to `vcm`, clear metrics, and clear `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, sample input amplitude and drive level.
- `P_APPLY_AN_AM_GAIN_COMPRESSION_PROXY`: Apply an AM gain compression proxy as drive increases.
- `P_APPLY_A_ONE_SAMPLE_MEMORY_TERM`: Apply a one-sample memory term that changes output polarity metric after large input changes.
- `P_EXPOSE_AM_AND_PM_PROXIES_SEPARATELY`: Expose AM and PM proxies separately and assert `valid` after the first update.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `pa_ampm_memory_tap_macro.va`.
Every supplied `.va` file is editable; do not add or omit files.
