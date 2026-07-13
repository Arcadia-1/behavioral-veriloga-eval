# Sample Hold Droop Front End Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Sample Hold Droop Front End` DUT. The evaluator runs the same submitted bytes
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

- `P_APERTURE_CAPTURE`: Each rising clk crossing schedules capture of vin after taperture rather than sampling at an unrelated time.
- `P_SUPPLY_CLAMPED_SAMPLE`: At aperture capture, the held output updates to the sampled vin clamped between the instantaneous vss and vdd rails.
- `P_COARSE_DECISION`: At each capture, coarse is high when the sampled value exceeds vth and low otherwise, then holds until the next capture.
- `P_VALID_PULSE`: Valid asserts at the aperture sample and deasserts after valid_width.
- `P_LOW_PHASE_DROOP`: While clk is low, vout applies bounded droop updates governed by tau and dt instead of remaining ideal or changing discontinuously.
- `P_NO_TRACK_THROUGH`: Between aperture captures, vout does not transparently track changes on vin; only the specified droop behavior is permitted.

The required trace names are: `time`, `vdd`, `vss`, `clk`, `vin`, `vout`, `valid`, `coarse`.

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
