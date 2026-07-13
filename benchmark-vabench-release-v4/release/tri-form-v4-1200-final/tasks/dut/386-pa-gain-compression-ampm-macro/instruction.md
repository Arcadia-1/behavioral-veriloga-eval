# PA Gain-compression and AM/PM Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `pa_gain_compression_ampm_macro.va`: `pa_gain_compression_ampm_macro`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` to `vcm`, clear metrics, and clear `compressed`.
- `P_WHEN_ENABLED_AMPLIFY_VIN_VCM_WITH`: When enabled, amplify `vin - vcm` with high small-signal gain at low envelope.
- `P_AS_ENVELOPE_EXCEEDS_THE_COMPRESSION_THRESHOLD`: As `envelope` exceeds the compression threshold, reduce the effective gain monotonically.
- `P_EXPOSE_THE_ACTIVE_GAIN_ON_GAIN`: Expose the active gain on `gain_metric` and a monotonic AM/PM proxy on `phase_metric`.
- `P_ASSERT_COMPRESSED_WHEN_THE_EFFECTIVE_GAIN`: Assert `compressed` when the effective gain is below the small-signal gain by the configured compression condition.
- `P_CLAMP_VOUT_INSIDE_VSS_VDD`: Clamp `vout` inside `[vss, vdd]`.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `pa_gain_compression_ampm_macro.va`.
Do not add or omit artifacts.
