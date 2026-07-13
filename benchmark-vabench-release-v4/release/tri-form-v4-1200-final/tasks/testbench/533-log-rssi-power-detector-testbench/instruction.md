# Log RSSI Power Detector Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Log RSSI Power Detector` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_BASELINE`: Initialization or active reset drives out to 0.12 V and metric to 0 V.
- `P_CLOCKED_MAGNITUDE_SAMPLE`: Each rising clk crossing while reset is inactive samples the magnitude abs(vin - 0.45 V); the held outputs do not track vin between samples.
- `P_RSSI_BINS`: Sampled magnitudes below 0.035 V, from 0.035 V to below 0.11 V, from 0.11 V to below 0.22 V, and at least 0.22 V map to out levels 0.12 V, 0.30 V, 0.54 V, and 0.72 V respectively.
- `P_AMPLITUDE_METRIC`: Metric equals three times the sampled magnitude, clamped to the 0 V to 0.9 V range.
- `P_OUTPUT_BOUNDS`: Out remains within the public 0.08 V to 0.82 V clamp range with finite transition smoothing.

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
