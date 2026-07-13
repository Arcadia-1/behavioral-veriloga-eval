# L2 7b DAC Ready Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `L2 7b DAC Ready` DUT. The evaluator runs the same submitted bytes
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

- `P_FIRST_READY_EDGE_ARMS_ONLY`: The first rising `rdy` edge arms the DAC and leaves the initialized output at zero.
- `P_READY_SAMPLES_SEVEN_BITS`: Each later rising `rdy` edge samples `din1..din7` against `vth` with the declared switched-capacitor weights.
- `P_BIPOLAR_WEIGHTED_DAC_OUTPUT`: Map the sampled 7-bit weight to the declared bipolar single-ended output with the correct denominator and offset.
- `P_DAC_OUTPUT_LEVEL_AND_HOLD`: Hold `aout` between ready edges and drive the declared voltage scale without half-level errors.

The required trace names are: `time`, `aout`, `din1`, `din2`, `din3`, `din4`, `din5`, `din6`, `din7`, `rdy`.

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
