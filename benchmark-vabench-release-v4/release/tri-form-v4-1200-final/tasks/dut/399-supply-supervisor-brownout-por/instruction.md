# Supply Supervisor with Brownout POR

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `supply_supervisor_brownout_por.va`: `supply_supervisor_brownout_por`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_SAFE`: Reset or disable asserts brownout, holds POR low, clears pgood and both metrics.
- `P_UVLO_HYSTERESIS`: Supply below uvlo_fall enters brownout and supply must exceed uvlo_rise to leave it.
- `P_RELEASE_DELAY`: POR and pgood assert only after release_cycles consecutive good rising clock edges.
- `P_DIP_RESTART`: A supply dip below uvlo_fall immediately reasserts brownout and clears release progress.
- `P_STATE_METRICS`: Delay and state metrics report the saturated release count and four public supervisor states.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `supply_supervisor_brownout_por.va`.
Do not add or omit artifacts.
