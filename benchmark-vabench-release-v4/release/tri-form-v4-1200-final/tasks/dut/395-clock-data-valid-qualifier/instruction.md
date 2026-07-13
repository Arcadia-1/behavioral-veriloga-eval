# Clock-and-data Valid Qualifier

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `clock_data_valid_qualifier.va`: `clock_data_valid_qualifier`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CLEAR`: Reset or disable clears valid, qualification, and the public age metric.
- `P_DATA_EDGE_RESTART`: Either polarity data edge restarts the age count at zero while enabled.
- `P_CLOCKED_AGE`: Each later rising clk edge increments age before qualification.
- `P_INCLUSIVE_WINDOW`: Ages one through max_age_cycles are qualified and older ages are not.
- `P_REGISTERED_METRIC`: valid_out is the registered qualified state and the metric reports saturated normalized age.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `clock_data_valid_qualifier.va`.
Do not add or omit artifacts.
