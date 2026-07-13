# Charge Pump Abstraction Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Charge Pump Abstraction` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_MIDSCALE`: When rst is high, vctrl resets to the midpoint of vmin and vmax and metric is 0.45 V.
- `P_UP_ONLY_STEP`: A rising clock crossing sampling up high and dn low increases vctrl by step and encodes metric at 0.75 V.
- `P_DN_ONLY_STEP`: A rising clock crossing sampling dn high and up low decreases vctrl by step and encodes metric at 0.15 V.
- `P_HOLD_CASES`: A rising clock crossing sampling both or neither request holds vctrl and encodes metric at 0.45 V.
- `P_CONTROL_CLAMP`: Repeated sampled movement cannot drive vctrl below vmin or above vmax.
- `P_SAMPLED_HOLD`: Changes on up or dn between rising clock crossings do not immediately change vctrl.

The required trace names are: `time`, `clk`, `rst`, `up`, `dn`, `vctrl`, `metric`.

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
