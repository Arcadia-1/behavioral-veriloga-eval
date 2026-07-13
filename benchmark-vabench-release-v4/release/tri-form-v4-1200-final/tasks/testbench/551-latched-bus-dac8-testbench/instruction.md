# Latched Bus DAC8 Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Latched Bus DAC8` DUT. The evaluator runs the same submitted bytes
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

- `P_RISING_EDGE_CAPTURE`: Each rising crossing of vclk through vth captures the unsigned value of b[7:0].
- `P_HOLD_BETWEEN_EDGES`: vout retains the value from the most recent rising clock crossing despite input-bus changes between update edges.
- `P_ENDPOINTS`: Latched code 0 maps to 0 V and latched code 255 maps to vref.
- `P_BINARY_MONOTONICITY`: Increasing the latched unsigned code never decreases vout, with b7 as MSB and b0 as LSB.
- `P_OUTPUT_SMOOTHING`: vout approaches each newly latched target with finite transition smoothing set by tr.

The required trace names are: `time`, `vclk`, `b7`, `b6`, `b5`, `b4`, `b3`, `b2`, `b1`, `b0`, `vout`.

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
