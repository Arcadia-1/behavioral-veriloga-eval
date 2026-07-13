# PA Gain-compression and AM/PM Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `pa_gain_compression_ampm_macro.va`: `pa_gain_compression_ampm_macro`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` to `vcm`, clear metrics, and clear `compressed`.
- `P_WHEN_ENABLED_AMPLIFY_VIN_VCM_WITH`: When enabled, amplify `vin - vcm` with high small-signal gain at low envelope.
- `P_AS_ENVELOPE_EXCEEDS_THE_COMPRESSION_THRESHOLD`: As `envelope` exceeds the compression threshold, reduce the effective gain monotonically.
- `P_EXPOSE_THE_ACTIVE_GAIN_ON_GAIN`: Expose the active gain on `gain_metric` and a monotonic AM/PM proxy on `phase_metric`.
- `P_ASSERT_COMPRESSED_WHEN_THE_EFFECTIVE_GAIN`: Assert `compressed` when the effective gain is below the small-signal gain by the configured compression condition.
- `P_CLAMP_VOUT_INSIDE_VSS_VDD`: Clamp `vout` inside `[vss, vdd]`.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `pa_gain_compression_ampm_macro.va`.
Every supplied `.va` file is editable; do not add or omit files.
