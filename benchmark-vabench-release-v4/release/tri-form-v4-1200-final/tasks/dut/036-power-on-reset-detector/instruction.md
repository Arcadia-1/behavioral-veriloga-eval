# Power-On Reset Detector

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `power_on_reset_detector.va`: `power_on_reset_detector`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_ASSERTED_UNSAFE`: Out is active-high reset and remains asserted while rst is high or vin is below vtrip.
- `P_DELAYED_RELEASE`: After rst releases and vin is power-good, out stays asserted for four rising clk updates before deasserting.
- `P_RELEASE_STATUS`: Metric uses an intermediate status level during the release delay, is high after delayed reset release completes, and is cleared when reset is reasserted or supply is not power-good.
- `P_FAULT_REASSERTION`: A new reset assertion or a brownout below vtrip immediately reasserts out and clears the accumulated release delay, independent of the next clk edge.
- `P_VOLTAGE_CODED_LEVELS`: Out and metric use bounded voltage-coded low and high levels with finite transition smoothing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `power_on_reset_detector.va`.
Do not add or omit artifacts.
