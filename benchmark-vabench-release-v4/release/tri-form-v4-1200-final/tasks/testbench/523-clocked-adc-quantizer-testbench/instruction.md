# Clocked ADC Quantizer Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Clocked ADC Quantizer` DUT. The evaluator runs the same submitted bytes
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

- `P_RISING_EDGE_QUANTIZATION`: At each rising CLK crossing, VIN is quantized into one of eight uniform bins spanning vrefn to vrefp.
- `P_CODE_CLAMP`: Samples at or outside the conversion endpoints produce codes clamped to the inclusive range 0 through 7.
- `P_BINARY_RAIL_ENCODING`: DOUT2 through DOUT0 encode the held code from MSB to LSB using VDD for one and VSS for zero.
- `P_CODE_MONOTONICITY`: For increasing VIN samples across the conversion range, the sampled three-bit code is nondecreasing.
- `P_SAMPLE_HOLD`: The output code remains stable between rising CLK crossings even when VIN changes.

The required trace names are: `time`, `vdd`, `vss`, `vin`, `clk`, `dout2`, `dout1`, `dout0`.

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
