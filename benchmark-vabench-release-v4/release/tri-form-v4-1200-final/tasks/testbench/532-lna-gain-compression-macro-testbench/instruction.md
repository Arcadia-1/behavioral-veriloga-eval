# LNA Gain Compression Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `LNA Gain Compression Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_INITIAL_AND_RESET_COMMON_MODE`: Initialization sets out to 0.45 V and clears metric; an active-high reset sampled on a rising clk crossing restores the same state.
- `P_SMALL_SIGNAL_GAIN`: For linear values from 0.14 V through 0.76 V, out equals 0.45 V plus gain times the sampled vin deviation and metric is 0.1 V.
- `P_POSITIVE_COMPRESSION`: Above linear 0.76 V, excess signal is compressed by factor 0.28 and metric is 0.8 V.
- `P_NEGATIVE_COMPRESSION`: Below linear 0.14 V, excess signal is compressed by factor 0.28 and metric is 0.8 V.
- `P_FINAL_OUTPUT_CLAMP`: The final held output remains within 0.04 V through 0.86 V.
- `P_CLOCKED_HOLD`: Out and metric update on rising clock crossings and hold between samples.

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
