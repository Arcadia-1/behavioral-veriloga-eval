# Differential Common Mode Window Monitor Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Differential Common Mode Window Monitor` DUT. The evaluator runs the same submitted bytes
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

- `P_CONTINUOUSLY_COMPUTE_VDIFF_V_VIP_V`: Continuously compute `vdiff = V(vip) - V(vin)` and `vcm = 0.5 * (V(vip) + V(vin))`. Drive `diff_ok` high only while `en` is high and `abs(vdiff)` is no larger than `diff_max`. Drive `cm_ok` high only while `en` is high and `abs(vcm - V(vcm_ref))` is no larger than `cm_tol`. Drive `valid` high only when both `diff_ok` and `cm_ok` would be high. Drive `diff_metric` as `vhi * clip(abs(vdiff) / diff_fullscale, 0, 1)` and `cm_metric` as `vhi * clip(abs(vcm - V(vcm_ref)) / cm_fullscale, 0, 1)`. Smooth the voltage-coded Boolean outputs with `transition()`.
- `P_BUILD_A_VOLTAGE_DOMAIN_INPUT_VALIDITY`: Build a voltage-domain input-validity monitor for a differential analog front-end. The module checks whether the differential input magnitude remains inside a public linear range, whether the instantaneous common-mode level stays near a reference, and whether the enabled input pair is valid for downstream behavioral processing.
- `P_VTH_0_45_V_LOGIC_THRESHOLD`: `vth = 0.45 V`: logic threshold for `en`.
- `P_VHI_0_9_V_HIGH_LEVEL`: `vhi = 0.9 V`: high level for voltage-coded outputs.
- `P_DIFF_MAX_0_30_V_MAXIMUM`: `diff_max = 0.30 V`: maximum allowed `abs(V(vip) - V(vin))`.
- `P_DIFF_FULLSCALE_0_45_V_FULL`: `diff_fullscale = 0.45 V`: full-scale value for `diff_metric`.

The required trace names are: `time`, `cm_metric`, `cm_ok`, `diff_metric`, `diff_ok`, `en`, `valid`, `vcm_ref`, `vin`, `vip`.

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
