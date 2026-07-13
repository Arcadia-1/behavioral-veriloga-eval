# Supply Bias Validity Gate Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `supply_bias_validity_gate.va`: `supply_bias_validity_gate`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_MODEL_A_REUSABLE_SUPPLY_BIAS_VALIDITY`: Model a reusable supply/bias validity gate for a behavioral AMS block. Drive `ok` high only when the local supply is inside the supply window, the local ground rail is close enough to the global reference, and the bias input is inside its `vss`-referenced window. Drive `gated` high only when `ok` is high, `en` is high, and `pd` is low. Both outputs must be voltage-coded and smoothed with `transition()`.
- `P_BUILD_A_VOLTAGE_DOMAIN_BIAS_REFERENCE`: Build a voltage-domain bias/reference/power-management DUT. The module reports whether local supply, local ground, and local bias conditions are valid, then gates a downstream drive-enable output with public enable and power-down inputs.
- `P_VTH_0_45_V_LOGIC_THRESHOLD`: `vth = 0.45 V`: logic threshold for `en` and `pd`.
- `P_VHI_0_9_V_HIGH_LEVEL`: `vhi = 0.9 V`: high level for `ok` and `gated`.
- `P_VDD_MIN_0_75_V_VDD`: `vdd_min = 0.75 V`, `vdd_max = 1.05 V`: valid supply-voltage window measured
- `P_VSS_MAX_0_08_V_MAXIMUM`: `vss_max = 0.08 V`: maximum absolute ground-rail displacement allowed for

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `supply_bias_validity_gate.va`.
Every supplied `.va` file is editable; do not add or omit files.
