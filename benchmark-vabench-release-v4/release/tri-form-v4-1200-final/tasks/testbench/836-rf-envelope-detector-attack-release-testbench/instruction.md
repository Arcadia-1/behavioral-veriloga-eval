# RF Envelope Detector with Attack/Release Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `RF Envelope Detector with Attack/Release` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, clear envelope, metric, and `valid`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: On each enabled rising `clk` edge, estimate input magnitude as distance from `vcm`.
- `P_USE_A_FASTER_ATTACK_STEP_WHEN`: Use a faster attack step when magnitude rises and a slower release step when it falls.
- `P_DRIVE_ENVELOPE_WITH_THE_TRACKED_MAGNITUDE`: Drive `envelope` with the tracked magnitude mapped into the public voltage range.
- `P_EXPOSE_WHETHER_THE_LAST_UPDATE_USED`: Expose whether the last update used attack or release on `attack_metric`.

The required trace names are: `time`, `vin`, `clk`, `rst`, `enable`, `envelope`, `attack_metric`, `valid`.

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
