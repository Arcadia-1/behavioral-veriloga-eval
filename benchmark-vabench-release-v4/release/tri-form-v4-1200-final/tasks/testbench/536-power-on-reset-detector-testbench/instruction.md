# Power-On Reset Detector Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Power-On Reset Detector` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_ASSERTED_UNSAFE`: Out is active-high reset and remains asserted while rst is high or vin is below vtrip.
- `P_DELAYED_RELEASE`: After rst releases and vin is power-good, out stays asserted for four rising clk updates before deasserting.
- `P_RELEASE_STATUS`: Metric uses an intermediate status level during the release delay, is high after delayed reset release completes, and is cleared when reset is reasserted or supply is not power-good.
- `P_FAULT_REASSERTION`: A new reset assertion or a brownout below vtrip immediately reasserts out and clears the accumulated release delay, independent of the next clk edge.
- `P_VOLTAGE_CODED_LEVELS`: Out and metric use bounded voltage-coded low and high levels with finite transition smoothing.

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
