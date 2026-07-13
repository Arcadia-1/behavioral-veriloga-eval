# Common-gate TIA Front-end Macro Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `common_gate_tia_front_end.va`: `common_gate_tia_front_end`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` to `vcm` and clear the metrics.
- `P_TREAT_VIN_PROXY_AS_A_VOLTAGE`: Treat `vin_proxy` as a voltage-domain proxy for input current magnitude.
- `P_GENERATE_AN_OUTPUT_DEVIATION_AROUND_VCM`: Generate an output deviation around `vcm` proportional to the proxy input and `rz_gain`.
- `P_REDUCE_EFFECTIVE_GAIN_WHEN_BIAS_FALLS`: Reduce effective gain when `bias` falls below `bias_min` and expose the effective gain on `transimpedance_metric`.
- `P_ASSERT_OVERLOAD_WHEN_THE_UNCLAMPED_OUTPUT`: Assert `overload` when the unclamped output target would exceed the rails.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `common_gate_tia_front_end.va`.
Every supplied `.va` file is editable; do not add or omit files.
