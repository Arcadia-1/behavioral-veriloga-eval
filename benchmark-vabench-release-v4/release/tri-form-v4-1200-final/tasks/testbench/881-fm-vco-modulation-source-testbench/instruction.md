# FM/VCO Modulation Source Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `FM/VCO Modulation Source Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `osc_out`, `freq_metric`, `phase_marker`, and `valid` low.
- `P_WHEN_ENABLED_GENERATE_A_DETERMINISTIC_BEHAVIOR`: When enabled, generate a deterministic behavioral oscillator whose frequency increases monotonically with `mod_in`.
- `P_CLAMP_THE_COMMANDED_FREQUENCY_TO_A`: Clamp the commanded frequency to a nonnegative range and expose the normalized command on `freq_metric`.
- `P_OSC_OUT_MUST_TOGGLE_BETWEEN_VSS`: `osc_out` must toggle between `vss` and `vdd` according to the commanded oscillator state.
- `P_PHASE_MARKER_MUST_PULSE_OR_TOGGLE`: `phase_marker` must pulse or toggle once per oscillator cycle so cycle period order is observable from public behavior.
- `P_ASSERT_VALID_AFTER_THE_FIRST_COMPLETED`: Assert `valid` after the first completed oscillator cycle following enable.

The required trace names are: `time`, `mod_in`, `enable`, `rst`, `osc_out`, `freq_metric`, `phase_marker`, `valid`.

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
