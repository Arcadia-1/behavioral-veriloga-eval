# Common-gate TIA Front-end Macro Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Common-gate TIA Front-end Macro` DUT. The evaluator runs the same submitted bytes
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

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` to `vcm` and clear the metrics.
- `P_TREAT_VIN_PROXY_AS_A_VOLTAGE`: Treat `vin_proxy` as a voltage-domain proxy for input current magnitude.
- `P_GENERATE_AN_OUTPUT_DEVIATION_AROUND_VCM`: Generate an output deviation around `vcm` proportional to the proxy input and `rz_gain`.
- `P_REDUCE_EFFECTIVE_GAIN_WHEN_BIAS_FALLS`: Reduce effective gain when `bias` falls below `bias_min` and expose the effective gain on `transimpedance_metric`.
- `P_ASSERT_OVERLOAD_WHEN_THE_UNCLAMPED_OUTPUT`: Assert `overload` when the unclamped output target would exceed the rails.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

The required trace names are: `time`, `vin_proxy`, `bias`, `enable`, `rst`, `vout`, `transimpedance_metric`, `overload`.

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
