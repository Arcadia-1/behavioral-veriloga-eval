# DAC Serial Accumulator Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `DAC Serial Accumulator` DUT. The evaluator runs the same submitted bytes
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

- `P_SAMPLE_CLOCK_RESET`: Each falling `clk_sample` crossing resets the accumulator and serial bit counter.
- `P_SARREADY_SERIAL_ACCUMULATION`: Falling `clk_sarready` crossings during the active bit window add the sampled `data` bit to the accumulator.
- `P_BINARY_WEIGHT_ORDER`: The first accepted serial bit has the largest binary weight and later bits use descending weights.
- `P_BIPOLAR_OUTPUT_MAPPING`: The accumulated code is mapped to the required bipolar output range rather than an unipolar code.

The required trace names are: `time`, `clk_sample`, `clk_sarready`, `data`, `out`.

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
