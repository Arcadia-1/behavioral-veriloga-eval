# LNA Gain-compression Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `lna_gain_compression_macro.va`: `lna_gain_compression_macro`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` to `vcm`, clear `gain_metric`, and clear `compression_flag`.
- `P_WHEN_ENABLED_PROVIDE_HIGH_GAIN_FOR`: When enabled, provide high gain for small input deviations around `vcm`.
- `P_REDUCE_EFFECTIVE_GAIN_MONOTONICALLY_WHEN_THE`: Reduce effective gain monotonically when the absolute input deviation exceeds `input_clip`.
- `P_EXPOSE_ACTIVE_GAIN_ON_GAIN_METRIC`: Expose active gain on `gain_metric` and assert `compression_flag` during compressed operation.
- `P_CLAMP_VOUT_INSIDE_VSS_VDD`: Clamp `vout` inside `[vss, vdd]`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `lna_gain_compression_macro.va`.
Every supplied `.va` file is editable; do not add or omit files.
