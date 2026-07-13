# Foreground RDAC Calibrator Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Foreground RDAC Calibrator` DUT. The evaluator runs the same submitted bytes
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

- `P_INITIAL_MSB_TRIAL_CODE`: At startup, calibration is active with `dc6` asserted and all lower RDAC bits deasserted.
- `P_CLOCKED_RDAC_DECISION_SEQUENCE`: On each rising `ck` crossing while active, resolve the current trial bit from `d` versus `vth` and advance from MSB to LSB.
- `P_DECISION_POLARITY`: Comparator-low and comparator-high decisions update the trial bit in the declared polarity without inverting the search direction.
- `P_CALIBRATION_COMPLETION`: After the final RDAC decision, deassert calibration enable and hold the completed code.
- `P_RDAC_OUTPUT_LEVELS`: All RDAC code and enable outputs remain voltage-coded at valid low/high levels.

The required trace names are: `time`, `ck`, `cvinn`, `cvinp`, `d`, `dc0`, `dc1`, `dc2`, `dc3`, `dc4`, `dc5`, `dc6`, `en`, `enb`, `vrefn`, `vrefp`.

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
