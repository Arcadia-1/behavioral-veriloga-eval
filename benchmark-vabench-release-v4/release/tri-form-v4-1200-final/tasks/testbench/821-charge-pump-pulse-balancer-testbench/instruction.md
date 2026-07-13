# Charge-pump Pulse Balancer Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Charge-pump Pulse Balancer` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vctrl` to `vcm`, clear imbalance, and clear `balanced`.
- `P_ON_EACH_RISING_CLK_EDGE_OBSERVE`: On each rising `clk` edge, observe voltage-coded `up` and `dn` pulse states.
- `P_INCREASE_VCTRL_FOR_UP_ONLY_DECREASE`: Increase `vctrl` for UP-only, decrease it for DN-only, and hold for simultaneous or inactive pulses.
- `P_DRIVE_IMBALANCE_METRIC_FROM_THE_ACCUMULATED`: Drive `imbalance_metric` from the accumulated UP-minus-DN activity.
- `P_ASSERT_BALANCED_ONLY_WHEN_THE_RECENT`: Assert `balanced` only when the recent absolute imbalance is below `balance_tol`.

The required trace names are: `time`, `up`, `dn`, `clk`, `rst`, `enable`, `vctrl`, `imbalance_metric`, `balanced`.

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
