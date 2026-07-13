# Aperture Delay Track And Hold Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Aperture Delay Track And Hold` DUT. The evaluator runs the same submitted bytes
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

- `P_INITIAL_VALUE`: At initialization, the held output is established from the initial observed vin value.
- `P_APERTURE_ARM`: Each rising crossing of clk through vth arms exactly one sample for the corresponding delayed aperture instant.
- `P_DELAYED_CAPTURE`: At taperture after the rising clk crossing, vout captures the vin value present at that delayed instant rather than at the clock edge.
- `P_HOLD`: Between delayed aperture instants, vout retains the most recently captured value and does not track vin.
- `P_RAIL_OBSERVABILITY`: VDD and VSS are public supply-observation ports for harness compatibility only; they do not clamp, scale, or shift the captured vin value.
- `P_OUTPUT_SMOOTHING`: Changes in the held value appear on vout with finite transition smoothing set by tedge.

The required trace names are: `time`, `vin`, `clk`, `vout`, `VDD`, `VSS`.

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
