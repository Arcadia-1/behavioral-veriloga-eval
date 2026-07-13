# AM Modulator Source Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `am_modulator_source_macro.va`: `am_modulator_source_macro`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` to `vcm`, clear `envelope_dbg`, and clear `valid`.
- `P_WHEN_ENABLED_TREAT_CARRIER_IN_AND`: When enabled, treat `carrier_in` and `mod_in` as deviations around `vcm`.
- `P_DRIVE_AN_AMPLITUDE_MODULATED_OUTPUT_WHOSE`: Drive an amplitude-modulated output whose carrier deviation increases when `mod_in` rises above `vcm` and decreases when it falls below `vcm`.
- `P_CLAMP_THE_ENVELOPE_MULTIPLIER_SO_THE`: Clamp the envelope multiplier so the output stays within `[vss, vdd]`.
- `P_ENVELOPE_DBG_MUST_EXPOSE_THE_ACTIVE`: `envelope_dbg` must expose the active voltage-domain envelope multiplier mapped into the output voltage range.
- `P_ASSERT_VALID_WHILE_ENABLED_AFTER_RESET`: Assert `valid` while enabled after reset has been released.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `am_modulator_source_macro.va`.
Every supplied `.va` file is editable; do not add or omit files.
