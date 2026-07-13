# Time Diff Detector Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Time Diff Detector` DUT. The evaluator runs the same submitted bytes
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

- `P_FIRST_EDGE_CAPTURE`: Within each clock window, only the first rising vinp crossing and first rising vinn crossing through vth_in define the stored timing measurement.
- `P_PREVIOUS_WINDOW_REPORT`: At each rising clk crossing through vth_clk, vout reports the edge-time difference captured in the preceding valid clock window; if either input edge was absent, vout holds its previous value.
- `P_SIGNED_DIFFERENCE`: The reported value preserves the sign of the vinp first-edge time minus the vinn first-edge time and applies the public scale factor.
- `P_OUTPUT_CLIP`: The scaled reported voltage is bounded to the closed interval from -vdd to +vdd.
- `P_WINDOW_REARM`: Each reporting clock edge rearms both input-edge detectors so the next window is measured independently.
- `P_OUTPUT_TRANSITION`: Reported output changes use the declared td delay and tr transition time.

The required trace names are: `time`, `clk`, `vinp`, `vinn`, `vout`.

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
