# RF Mixer Downconverter Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `RF Mixer Downconverter Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_COMMON_MODE`: Active reset drives out to 0.45 V common mode and metric low.
- `P_LO_POLARITY`: With reset inactive, clk above vth selects LO coefficient +1 and clk at or below vth selects coefficient -1.
- `P_DOWNCONVERSION_TRANSFER`: The baseband target is 0.45 V plus conv_gain times vin minus 0.45 V times the selected LO coefficient.
- `P_ACTIVE_METRIC`: Metric is 0.9 V while reset is inactive and conversion is active, and low during reset.
- `P_OUTPUT_CLAMP`: Out is clamped to 0.02 V through 0.88 V and changes with finite smoothing.

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
