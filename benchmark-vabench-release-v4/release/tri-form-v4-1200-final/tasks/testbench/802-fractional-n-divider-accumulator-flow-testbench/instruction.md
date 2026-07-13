# Fractional-N Divider Accumulator Flow Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Fractional-N Divider Accumulator Flow` DUT. The evaluator runs the same submitted bytes
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

- `P_USE_REF_CLK_AS_THE_REFERENCE`: Use `ref_clk` as the reference timing input.
- `P_GENERATE_A_BEHAVIORAL_DCO_CLOCK_ON`: Generate a behavioral DCO clock on `dco_clk`.
- `P_GENERATE_FB_CLK_BY_TOGGLING_IT`: Generate `fb_clk` by toggling it after a DCO rising-edge count selected by a
- `P_UPDATE_A_BOUNDED_CONTROL_VOLTAGE_MONITOR`: Update a bounded control-voltage monitor on `vctrl_mon` from the PFD phase
- `P_DRIVE_LOCK_HIGH_AFTER_STABLE_TRACKING`: Drive `lock` high after stable tracking, low or unstable during the

The required trace names are: `time`, `ref_clk`, `fb_clk`, `dco_clk`, `vctrl_mon`, `lock`, `VDD`, `VSS`.

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
