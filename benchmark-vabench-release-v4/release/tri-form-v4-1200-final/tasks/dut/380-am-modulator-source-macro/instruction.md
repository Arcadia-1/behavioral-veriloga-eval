# AM Modulator Source Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `am_modulator_source_macro.va`: `am_modulator_source_macro`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` to `vcm`, clear `envelope_dbg`, and clear `valid`.
- `P_WHEN_ENABLED_TREAT_CARRIER_IN_AND`: When enabled, treat `carrier_in` and `mod_in` as deviations around `vcm`.
- `P_DRIVE_AN_AMPLITUDE_MODULATED_OUTPUT_WHOSE`: Drive an amplitude-modulated output whose carrier deviation increases when `mod_in` rises above `vcm` and decreases when it falls below `vcm`.
- `P_CLAMP_THE_ENVELOPE_MULTIPLIER_SO_THE`: Clamp the envelope multiplier so the output stays within `[vss, vdd]`.
- `P_ENVELOPE_DBG_MUST_EXPOSE_THE_ACTIVE`: `envelope_dbg` must expose the active voltage-domain envelope multiplier mapped into the output voltage range.
- `P_ASSERT_VALID_WHILE_ENABLED_AFTER_RESET`: Assert `valid` while enabled after reset has been released.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `am_modulator_source_macro.va`.
Do not add or omit artifacts.
