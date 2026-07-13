# LDO Load Step Recovery Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `LDO Load Step Recovery` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_REGULATION_STATE`: Active-high reset initializes out and target to 0.60 V, load_mon to 0.10 V, ctrl_mon to 0.50 V, metric to 0.9 V, and clears recovery progress.
- `P_BOUNDED_LOAD_AND_TARGET`: Each non-reset rising clk edge clips vin to 0 V through 0.9 V on load_mon and uses the public load-dependent target 0.61 V minus 0.025 times load.
- `P_CONTROL_MONITOR`: Ctrl_mon represents the public load and regulation-error control expression and remains clamped to 0.05 V through 0.85 V.
- `P_HEAVY_LOAD_DROOP`: A sampled load increase greater than 0.20 V causes the public 0.13 V transient droop before first-order recovery and restarts recovery qualification.
- `P_LIGHT_LOAD_KICK`: A sampled load decrease greater than 0.20 V causes the public 0.05 V light-load recovery kick before first-order recovery and restarts qualification.
- `P_RECOVERY_AND_SETTLING`: Every non-reset update applies the public 0.30 first-order recovery, clamps out to 0.20 V through 0.75 V, and sets metric high only after at least five updates with target error below 0.045 V.

The required trace names are: `time`, `clk`, `rst`, `vin`, `out`, `metric`, `load_mon`, `ctrl_mon`.

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
