# Dynamic Supply Level Driver Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Dynamic Supply Level Driver` DUT. The evaluator runs the same submitted bytes
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

- `P_MODEL_A_DYNAMIC_SUPPLY_ELECTRICAL_LEVEL`: Model a dynamic-supply electrical level driver. Compute the input level relative to the local rails, not global ground. When `V(vdd, vss)` is at least `vsup_min`, drive `out` to the local low or high rail-derived level according to whether the normalized input exceeds `vth_frac`. When the supply is below `vsup_min`, drive `out` to the local low level. Smooth the output with `transition()`.
- `P_BUILD_A_DYNAMIC_SUPPLY_VOLTAGE_DOMAIN`: Build a dynamic-supply voltage-domain level driver. The module thresholds its input relative to local supply rails, drives its output relative to those same rails, and falls back to the local low level when the supply is invalid.
- `P_VSUP_MIN_0_55_V_MINIMUM`: `vsup_min = 0.55 V`: minimum `V(vdd, vss)` required for normal operation.
- `P_VTH_FRAC_0_5_INPUT_THRESHOLD`: `vth_frac = 0.5`: input threshold expressed as a fraction of the local supply
- `P_VLO_FRAC_0_0_VHI_FRAC`: `vlo_frac = 0.0`, `vhi_frac = 1.0`: output low and high levels expressed as
- `P_TR_40P_OUTPUT_TRANSITION_SMOOTHING_TIME`: `tr = 40p`: output transition smoothing time.

The required trace names are: `time`, `din`, `out`, `vdd`, `vss`.

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
