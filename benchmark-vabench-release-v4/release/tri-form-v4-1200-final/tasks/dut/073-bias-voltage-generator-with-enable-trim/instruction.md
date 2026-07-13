# Bias Voltage Generator With Enable Trim

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `bias_voltage_generator_with_enable_trim.va`: `bias_voltage_generator_with_enable_trim`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CLOCKED_UPDATE`: Bias state changes are evaluated on rising clk crossings through vth and hold between clock updates.
- `P_DISABLE_RESET`: At an update, rst above vth or vin below 0.25 V disables the generator, returning out and metric to 0 V.
- `P_TRIM_TARGET`: When enabled, the target is 0.28 V plus 0.55 times (vin minus 0.25 V) divided by 0.65 V, clamped to 0.28 V through 0.82 V.
- `P_SETTLING`: At each enabled update, out advances by 45 percent of the remaining difference to the current target rather than jumping directly.
- `P_MONOTONIC_TRIM`: For otherwise equal enabled histories, a higher trim request produces a target and settled out value no lower than a smaller request.
- `P_ENABLE_METRIC`: metric approaches 0.9 V while enabled and 0 V while disabled, with transition smoothing set by tr.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `bias_voltage_generator_with_enable_trim.va`.
Do not add or omit artifacts.
