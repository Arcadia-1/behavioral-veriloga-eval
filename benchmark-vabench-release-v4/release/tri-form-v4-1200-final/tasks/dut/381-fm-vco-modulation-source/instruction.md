# FM/VCO Modulation Source Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `fm_vco_modulation_source.va`: `fm_vco_modulation_source`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `osc_out`, `freq_metric`, `phase_marker`, and `valid` low.
- `P_WHEN_ENABLED_GENERATE_A_DETERMINISTIC_BEHAVIOR`: When enabled, generate a deterministic behavioral oscillator whose frequency increases monotonically with `mod_in`.
- `P_CLAMP_THE_COMMANDED_FREQUENCY_TO_A`: Clamp the commanded frequency to a nonnegative range and expose the normalized command on `freq_metric`.
- `P_OSC_OUT_MUST_TOGGLE_BETWEEN_VSS`: `osc_out` must toggle between `vss` and `vdd` according to the commanded oscillator state.
- `P_PHASE_MARKER_MUST_PULSE_OR_TOGGLE`: `phase_marker` must pulse or toggle once per oscillator cycle so cycle period order is observable from public behavior.
- `P_ASSERT_VALID_AFTER_THE_FIRST_COMPLETED`: Assert `valid` after the first completed oscillator cycle following enable.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `fm_vco_modulation_source.va`.
Do not add or omit artifacts.
