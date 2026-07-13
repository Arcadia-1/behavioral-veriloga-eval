# L2 CDAC 4b Switch Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `L2 CDAC 4b Switch` DUT. The evaluator runs the same submitted bytes
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
- `P_READY_SAMPLES_FOUR_BITS`: Each later rising `rdy` edge samples `din1..din4` against `vth` with the declared switched weights.
- `P_SWITCHED_WEIGHT_DENOMINATOR`: Compute `switched_weight` and normalize by `8.5` before output scaling.
- `P_BIPOLAR_CDAC_OUTPUT`: Map the sampled ratio to `(switched_weight / 8.5) * 2.0 * vdd - vdd` and hold it between ready edges.

The required trace names are: `time`, `aout`, `din1`, `din2`, `din3`, `din4`, `rdy`.

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
