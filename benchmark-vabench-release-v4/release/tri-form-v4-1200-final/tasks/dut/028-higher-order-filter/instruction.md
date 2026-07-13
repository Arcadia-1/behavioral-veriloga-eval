# Clocked Cascaded Two-Pole Filter

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `higher_order_filter.va`: `higher_order_filter`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_COMMON_MODE_INITIAL_RESET`: Both cascaded states and observable out return to 0.45 V during initialization and active-high reset.
- `P_GAINED_BOUNDED_TARGET`: Each eligible rising edge forms a rail-bounded target from gain times the input deviation around 0.45 V.
- `P_TWO_POLE_SAMPLED_SETTLING`: Out follows the second of two cascaded alpha-weighted sampled low-pass states and therefore settles more slowly than a single direct update.
- `P_LAG_METRIC`: Metric exposes the centered lag between the two cascaded states during settling and returns toward its baseline after convergence.
- `P_SIGNAL_RANGE`: The driven output remains within the public 0 V through 0.9 V signal range.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `higher_order_filter.va`.
Do not add or omit artifacts.
