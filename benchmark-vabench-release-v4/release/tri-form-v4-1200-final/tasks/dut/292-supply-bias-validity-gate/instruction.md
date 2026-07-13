# Supply Bias Validity Gate

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `supply_bias_validity_gate.va`: `supply_bias_validity_gate`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_MODEL_A_REUSABLE_SUPPLY_BIAS_VALIDITY`: Model a reusable supply/bias validity gate for a behavioral AMS block. Drive `ok` high only when the local supply is inside the supply window, the local ground rail is close enough to the global reference, and the bias input is inside its `vss`-referenced window. Drive `gated` high only when `ok` is high, `en` is high, and `pd` is low. Both outputs must be voltage-coded and smoothed with `transition()`.
- `P_BUILD_A_VOLTAGE_DOMAIN_BIAS_REFERENCE`: Build a voltage-domain bias/reference/power-management DUT. The module reports whether local supply, local ground, and local bias conditions are valid, then gates a downstream drive-enable output with public enable and power-down inputs.
- `P_VTH_0_45_V_LOGIC_THRESHOLD`: `vth = 0.45 V`: logic threshold for `en` and `pd`.
- `P_VHI_0_9_V_HIGH_LEVEL`: `vhi = 0.9 V`: high level for `ok` and `gated`.
- `P_VDD_MIN_0_75_V_VDD`: `vdd_min = 0.75 V`, `vdd_max = 1.05 V`: valid supply-voltage window measured
- `P_VSS_MAX_0_08_V_MAXIMUM`: `vss_max = 0.08 V`: maximum absolute ground-rail displacement allowed for

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `supply_bias_validity_gate.va`.
Do not add or omit artifacts.
