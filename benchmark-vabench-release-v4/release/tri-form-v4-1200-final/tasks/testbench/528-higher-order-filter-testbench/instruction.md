# Clocked Cascaded Two-Pole Filter Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Clocked Cascaded Two-Pole Filter` DUT. The evaluator runs the same submitted bytes
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

- `P_COMMON_MODE_INITIAL_RESET`: Both cascaded states and observable out return to 0.45 V during initialization and active-high reset.
- `P_GAINED_BOUNDED_TARGET`: Each eligible rising edge forms a rail-bounded target from gain times the input deviation around 0.45 V.
- `P_TWO_POLE_SAMPLED_SETTLING`: Out follows the second of two cascaded alpha-weighted sampled low-pass states and therefore settles more slowly than a single direct update.
- `P_LAG_METRIC`: Metric exposes the centered lag between the two cascaded states during settling and returns toward its baseline after convergence.
- `P_SIGNAL_RANGE`: The driven output remains within the public 0 V through 0.9 V signal range.

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
