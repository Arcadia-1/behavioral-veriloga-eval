# Supply Bias Validity Gate Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Supply Bias Validity Gate` DUT. The evaluator runs the same submitted bytes
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

- `P_MODEL_A_REUSABLE_SUPPLY_BIAS_VALIDITY`: Model a reusable supply/bias validity gate for a behavioral AMS block. Drive `ok` high only when the local supply is inside the supply window, the local ground rail is close enough to the global reference, and the bias input is inside its `vss`-referenced window. Drive `gated` high only when `ok` is high, `en` is high, and `pd` is low. Both outputs must be voltage-coded and smoothed with `transition()`.
- `P_BUILD_A_VOLTAGE_DOMAIN_BIAS_REFERENCE`: Build a voltage-domain bias/reference/power-management DUT. The module reports whether local supply, local ground, and local bias conditions are valid, then gates a downstream drive-enable output with public enable and power-down inputs.
- `P_VTH_0_45_V_LOGIC_THRESHOLD`: `vth = 0.45 V`: logic threshold for `en` and `pd`.
- `P_VHI_0_9_V_HIGH_LEVEL`: `vhi = 0.9 V`: high level for `ok` and `gated`.
- `P_VDD_MIN_0_75_V_VDD`: `vdd_min = 0.75 V`, `vdd_max = 1.05 V`: valid supply-voltage window measured
- `P_VSS_MAX_0_08_V_MAXIMUM`: `vss_max = 0.08 V`: maximum absolute ground-rail displacement allowed for

The required trace names are: `time`, `en`, `gated`, `ok`, `pd`, `vbias`, `vdd`, `vss`.

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
