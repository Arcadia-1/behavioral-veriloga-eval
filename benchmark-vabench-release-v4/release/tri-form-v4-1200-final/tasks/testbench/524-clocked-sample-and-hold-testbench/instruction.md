# Clocked Sample And Hold Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Clocked Sample And Hold` DUT. The evaluator runs the same submitted bytes
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

- `P_RISING_EDGE_SAMPLE`: OUT acquires the IN voltage present at each rising CLK crossing through vth, subject only to transition smoothing; a discriminating testbench should make the IN value at rising crossings differ from the value present at nearby falling crossings.
- `P_INTERSAMPLE_HOLD`: OUT retains the most recently sampled value between rising CLK crossings, including across input changes that occur after the sampled rising edge and before the next rising edge.
- `P_NO_HIGH_PHASE_TRACKING`: Changes on IN while CLK remains high do not make OUT transparent before the next rising crossing; the testbench should include at least one mid-high-phase IN step and observe OUT before the following rising edge.
- `P_LOCAL_RAIL_REFERENCE`: The held analog voltage is driven as a smooth voltage-domain output referenced to the local VDD and VSS rails, so the testbench should keep the rails observable and avoid relying only on absolute-ground behavior.

The required trace names are: `time`, `vdd`, `vss`, `in`, `clk`, `out`.

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
