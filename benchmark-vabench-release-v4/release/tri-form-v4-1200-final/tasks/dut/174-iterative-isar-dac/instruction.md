# Iterative ISAR DAC

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `iterative_isar_dac.va`: `iterative_isar_dac`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_INITIAL_SEARCH_STATE`: At initialization and reset, `vdac` returns to zero and the search step returns to `range`.
- `P_COMPARATOR_POLARITY_UPDATE`: On each rising `clk` crossing while active, `dcmp > vth` steps `vdac` in the specified comparator-driven direction and low decisions step the opposite way.
- `P_RADIX_STEP_REDUCTION`: The search step is divided by the public radix after each active comparison until it reaches the LSB limit.
- `P_HELD_DAC_OUTPUT`: `vdac` holds the current iterative search value between reset and qualifying clock events.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `iterative_isar_dac.va`.
Do not add or omit artifacts.
