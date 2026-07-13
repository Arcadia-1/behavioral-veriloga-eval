# Common-gate TIA Front-end Macro

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `common_gate_tia_front_end.va`: `common_gate_tia_front_end`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_DRIVE`: On reset or when disabled, drive `vout` to `vcm` and clear the metrics.
- `P_TREAT_VIN_PROXY_AS_A_VOLTAGE`: Treat `vin_proxy` as a voltage-domain proxy for input current magnitude.
- `P_GENERATE_AN_OUTPUT_DEVIATION_AROUND_VCM`: Generate an output deviation around `vcm` proportional to the proxy input and `rz_gain`.
- `P_REDUCE_EFFECTIVE_GAIN_WHEN_BIAS_FALLS`: Reduce effective gain when `bias` falls below `bias_min` and expose the effective gain on `transimpedance_metric`.
- `P_ASSERT_OVERLOAD_WHEN_THE_UNCLAMPED_OUTPUT`: Assert `overload` when the unclamped output target would exceed the rails.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `common_gate_tia_front_end.va`.
Do not add or omit artifacts.
