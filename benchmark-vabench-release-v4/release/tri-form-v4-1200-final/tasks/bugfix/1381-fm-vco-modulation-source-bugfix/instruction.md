# FM/VCO Modulation Source Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `fm_vco_modulation_source.va`: `fm_vco_modulation_source`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `osc_out`, `freq_metric`, `phase_marker`, and `valid` low.
- `P_WHEN_ENABLED_GENERATE_A_DETERMINISTIC_BEHAVIOR`: When enabled, generate a deterministic behavioral oscillator whose frequency increases monotonically with `mod_in`.
- `P_CLAMP_THE_COMMANDED_FREQUENCY_TO_A`: Clamp the commanded frequency to a nonnegative range and expose the normalized command on `freq_metric`.
- `P_OSC_OUT_MUST_TOGGLE_BETWEEN_VSS`: `osc_out` must toggle between `vss` and `vdd` according to the commanded oscillator state.
- `P_PHASE_MARKER_MUST_PULSE_OR_TOGGLE`: `phase_marker` must pulse or toggle once per oscillator cycle so cycle period order is observable from public behavior.
- `P_ASSERT_VALID_AFTER_THE_FIRST_COMPLETED`: Assert `valid` after the first completed oscillator cycle following enable.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `fm_vco_modulation_source.va`.
Every supplied `.va` file is editable; do not add or omit files.
