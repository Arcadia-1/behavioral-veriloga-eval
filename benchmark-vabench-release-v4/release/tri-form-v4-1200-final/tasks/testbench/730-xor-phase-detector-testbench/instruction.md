# XOR Phase Detector Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `XOR Phase Detector` DUT. The evaluator runs the same submitted bytes
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

- `P_INTERPRET_REF_AND_FB_LOGIC_LEVELS`: Interpret `ref` and `fb` logic levels using a threshold of `vdd/2`.
- `P_DRIVE_UP_HIGH_WHEN_THE_INTERPRETED`: Drive `up` high when the interpreted `ref` and `fb` levels differ.
- `P_DRIVE_DOWN_HIGH_WHEN_THE_INTERPRETED`: Drive `down` high when the interpreted `ref` and `fb` levels match.
- `P_UPDATE_OUTPUTS_COMBINATIONALLY_FROM_THE_CURREN`: Update outputs combinationally from the current input voltages.

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
