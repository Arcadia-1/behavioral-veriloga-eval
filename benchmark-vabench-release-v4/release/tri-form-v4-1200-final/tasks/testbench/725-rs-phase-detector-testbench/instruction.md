# RS Phase Detector Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `RS Phase Detector` DUT. The evaluator runs the same submitted bytes
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

- `P_DETECT_RISING_REF_AND_FB_CROSSINGS`: Detect rising `ref` and `fb` crossings at `vdd/2`.
- `P_A_RISING_REF_EDGE_SETS_THE`: A rising `ref` edge sets the latch state so `up` is high and `down` is low.
- `P_A_RISING_FB_EDGE_RESETS_THE`: A rising `fb` edge resets the latch state so `up` is low and `down` is high.
- `P_HOLD_THE_MOST_RECENT_LATCH_STATE`: Hold the most recent latch state between qualifying input edges.
- `P_INITIALIZE_TO_THE_RESET_STATE_WITH`: Initialize to the reset state with `up` low and `down` high.

The required trace names are: `time`, `ref`, `fb`, `up`, `down`.

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
