# Power Mode Supply Current Metric Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Power Mode Supply Current Metric` DUT. The evaluator runs the same submitted bytes
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

- `P_DRIVE_ISUP_METRIC_AS_A_VOLTAGE`: Drive `isup_metric` as a voltage-coded supply-current estimate. The estimate must scale with the local supply ratio `V(vdd, vss) / vnom` clipped to the range `[0, 1.5]`. Normalize load as `V(load, vss) / vhi` clipped to `[0, 1]`. When the block is disabled or powered down, meaning `V(en) <= vth` or `V(pd) > vth`, drive `isup_metric = ipd * supply_scale`. Otherwise choose the active base metric as `iq1` when `V(mode) > vth` and `iq0` when `V(mode) <= vth`, then drive `isup_metric = (base_metric + load_gain * load_norm) * supply_scale`. The metric is not a real branch current; it is an observable behavioral macro-model output.
- `P_BUILD_A_VOLTAGE_DOMAIN_BIAS_REFERENCE`: Build a voltage-domain bias/reference/power-management macro-model metric. The module exposes an observable supply-current demand estimate as a voltage-coded output across enable, power-down, operating mode, load demand, and local supply conditions.
- `P_VTH_0_45_V_LOGIC_THRESHOLD`: `vth = 0.45 V`: logic threshold for `en`, `pd`, and `mode`.
- `P_VHI_0_9_V_FULL_SCALE`: `vhi = 0.9 V`: full-scale input level for `load`.
- `P_VNOM_0_9_V_NOMINAL_SUPPLY`: `vnom = 0.9 V`: nominal supply used for supply-ratio scaling.
- `P_IQ0_0_08_IQ1_0_14`: `iq0 = 0.08`, `iq1 = 0.14`: active quiescent metric levels for low and high

The required trace names are: `time`, `en`, `isup_metric`, `load`, `mode`, `pd`, `vdd`, `vss`.

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
