# PA Gain-compression and AM/PM Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `PA Gain-compression and AM/PM Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` to `vcm`, clear metrics, and clear `compressed`.
- `P_WHEN_ENABLED_AMPLIFY_VIN_VCM_WITH`: When enabled, amplify `vin - vcm` with high small-signal gain at low envelope.
- `P_AS_ENVELOPE_EXCEEDS_THE_COMPRESSION_THRESHOLD`: As `envelope` exceeds the compression threshold, reduce the effective gain monotonically.
- `P_EXPOSE_THE_ACTIVE_GAIN_ON_GAIN`: Expose the active gain on `gain_metric` and a monotonic AM/PM proxy on `phase_metric`.
- `P_ASSERT_COMPRESSED_WHEN_THE_EFFECTIVE_GAIN`: Assert `compressed` when the effective gain is below the small-signal gain by the configured compression condition.
- `P_CLAMP_VOUT_INSIDE_VSS_VDD`: Clamp `vout` inside `[vss, vdd]`.

The required trace names are: `time`, `vin`, `envelope`, `enable`, `rst`, `vout`, `gain_metric`, `phase_metric`, `compressed`.

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
