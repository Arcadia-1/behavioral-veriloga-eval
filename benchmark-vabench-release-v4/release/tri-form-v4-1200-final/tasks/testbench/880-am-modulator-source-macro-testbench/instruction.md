# AM Modulator Source Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `AM Modulator Source Macro` DUT. The evaluator runs the same submitted bytes
against the correct DUT and five anonymous semantic negative DUTs. Your
testbench must accept the correct DUT and expose all five behavioral faults.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

The exact read-only source paths, modules, ports, instance names, and ordered
terminal bindings are declared in `solver_contract.json`.

## Public Parameter Contract

Honor the public parameter declarations in `solver_contract.json` when choosing
stimulus and coverage.

## Required Behavior

Create stimulus and save traces sufficient for the fixed evaluator oracle to check:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` to `vcm`, clear `envelope_dbg`, and clear `valid`.
- `P_WHEN_ENABLED_TREAT_CARRIER_IN_AND`: When enabled, treat `carrier_in` and `mod_in` as deviations around `vcm`.
- `P_DRIVE_AN_AMPLITUDE_MODULATED_OUTPUT_WHOSE`: Drive an amplitude-modulated output whose carrier deviation increases when `mod_in` rises above `vcm` and decreases when it falls below `vcm`.
- `P_CLAMP_THE_ENVELOPE_MULTIPLIER_SO_THE`: Clamp the envelope multiplier so the output stays within `[vss, vdd]`.
- `P_ENVELOPE_DBG_MUST_EXPOSE_THE_ACTIVE`: `envelope_dbg` must expose the active voltage-domain envelope multiplier mapped into the output voltage range.
- `P_ASSERT_VALID_WHILE_ENABLED_AFTER_RESET`: Assert `valid` while enabled after reset has been released.

The required trace names are: `time`, `carrier_in`, `mod_in`, `enable`, `rst`, `vout`, `envelope_dbg`, `valid`.

## Modeling Constraints

- Submit one self-contained top-level transient `.scs` file.
- Use only the exact declared testbench include paths and public DUT interfaces.
- Do not redefine the DUT, drive declared DUT outputs, inspect private internals,
  access undeclared files, or emit a self-reported result.
- Respect every public resource limit in `solver_contract.json`.
- Missing traces, setup errors, and invalid runs do not count as behavioral kills.

## Output Contract

Return exactly one submission-root-relative artifact named `testbench.scs`. Do not return a DUT,
checker, script, data file, waveform, or auxiliary deck.
