# Non-overlapping Clock Generator

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `nonoverlap_clock_generator.va`: `nonoverlap_clock_generator`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_OR_A_LOW_ENABLE_CLEARS`: Reset or a low `enable` clears both phases, `deadtime_metric`, and `valid`.
- `P_A_RISING_CLK_IN_REQUEST_EVENTUALLY`: A rising `clk_in` request eventually enables `phi1`; a falling `clk_in` request eventually enables `phi2`.
- `P_DURING_EACH_HANDOFF_BOTH_PHI1_AND`: During each handoff, both `phi1` and `phi2` remain low for the configured dead-time interval.
- `P_PHI1_AND_PHI2_MUST_NEVER_BE`: `phi1` and `phi2` must never be high at the same time.
- `P_DEADTIME_METRIC_IS_HIGH_ONLY_WHILE`: `deadtime_metric` is high only while a pending phase request is in the enforced both-low interval.
- `P_VALID_BECOMES_HIGH_AFTER_THE_FIRST`: `valid` becomes high after the first enabled handoff completes and remains high until reset or disable.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `nonoverlap_clock_generator.va`.
Do not add or omit artifacts.
