# Reference Startup Enable Flow

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `reference_startup_enable_flow.va`: `reference_startup_enable_flow`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_SUPPLY_AND_ENABLE_MONITORS`: Supply_ok is 0.9 V exactly when vdd_in exceeds 0.32 V, while enable_mon is 0.9 V exactly when en exceeds vth.
- `P_RESET_OR_BROWNOUT`: Active reset or a bad supply clears out, metric, startup progress, and state; a supply dip also removes valid status.
- `P_DISABLED_REFERENCE`: With supply good and enable low, out is 0.05 V, metric is 0.1 V, startup progress is cleared, and state_mon represents state 1.
- `P_ENABLED_SETTLING`: On each rising clk crossing with supply good and enable high, out advances by 0.32 times its remaining error to 0.55 V and the startup count increments up to 8.
- `P_STARTUP_VALIDITY`: During enabled startup metric is 0.25 V and state is 2; after at least five enabled updates with out above 0.48 V, metric is 0.9 V and state is 3.
- `P_BROWNOUT_RECOVERY`: After a supply dip and restoration with enable asserted, the output and monitors repeat the same startup sequence before returning valid.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `reference_startup_enable_flow.va`.
Do not add or omit artifacts.
