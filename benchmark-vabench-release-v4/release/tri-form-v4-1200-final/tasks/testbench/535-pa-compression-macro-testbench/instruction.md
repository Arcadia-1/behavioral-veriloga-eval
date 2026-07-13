# PA Compression Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `PA Compression Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_COMMON_MODE`: Initialization or active reset returns out to 0.45 V common mode and clears metric to 0 V.
- `P_CLOCKED_UPDATE`: Out and metric update from the sampled signed drive vin - 0.45 V on rising clk crossings and hold between updates.
- `P_LINEAR_REGION`: When 0.45 V + gain*(vin - 0.45 V) lies from 0.12 V through 0.78 V, out equals that target and metric is 0.1 V.
- `P_SYMMETRIC_COMPRESSION`: Targets above 0.78 V or below 0.12 V are compressed with slope 0.18 about the corresponding boundary, and metric is 0.85 V.
- `P_OUTPUT_CLAMP`: The compressed output remains within 0.02 V through 0.88 V with finite transition smoothing.

The required trace names are: `time`, `clk`, `rst`, `vin`, `out`, `metric`.

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
