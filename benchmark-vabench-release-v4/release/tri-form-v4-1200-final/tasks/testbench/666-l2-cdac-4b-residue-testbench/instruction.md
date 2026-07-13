# L2 CDAC 4b Residue Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `L2 CDAC 4b Residue` DUT. The evaluator runs the same submitted bytes
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

- `P_FALLING_CLOCK_SAMPLE`: `vin` is sampled into the residue on initial step and on falling `clks` crossings through `vdd/2`.
- `P_CONTROL_STEP_WEIGHTS`: Rising control crossings add positive capacitive reference steps: `dctrl3` is half scale, `dctrl2` quarter scale, and `dctrl1` eighth scale.
- `P_RETAINED_RESIDUE_OUTPUT`: `vres` retains the accumulated sampled residue between clock/control events.

The required trace names are: `time`, `vin`, `clks`, `dctrl1`, `dctrl2`, `dctrl3`, `vres`.

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
