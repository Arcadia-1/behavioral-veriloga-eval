# First Order Sigma Delta Modulator Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `First Order Sigma Delta Modulator` DUT. The evaluator runs the same submitted bytes
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

- `P_RISING_EDGE_UPDATE`: The one-bit output state updates only from accumulator decisions made on rising crossings of vclk through vth_clk.
- `P_FIRST_ORDER_FEEDBACK`: Each clocked decision reflects accumulation of the current normalized input minus the previous one-bit feedback state.
- `P_BINARY_OUTPUT`: bitout is voltage-coded low near 0 V or high near vh with finite transition smoothing.
- `P_INPUT_DENSITY_ORDER`: Over a sufficiently long common observation interval, a larger constant vin produces a nondecreasing fraction of high output bits.
- `P_FEEDBACK_STABILITY`: For an in-range constant input, the output stream continues to alternate as needed rather than running away as an open-loop accumulator.

The required trace names are: `time`, `vin`, `vclk`, `bitout`.

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
