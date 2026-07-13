# Latched Comparator Delay

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `latched_comparator_delay.va`: `latched_comparator_delay`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_SUPPLY_REFERENCED_THRESHOLD`: The latch clock threshold is the midpoint of VDD and GND, and DOUT low and high levels use those same rails.
- `P_RISING_EDGE_LATCH`: Each rising CLK midpoint crossing latches one comparison result; falling crossings do not resample the input.
- `P_OFFSET_DECISION`: With vn zero, DOUT latches high exactly when VINP minus VINN exceeds vos and low otherwise.
- `P_SEEDED_RANDOM_TERM`: With vn nonzero, each latch decision includes a normal input-referred term scaled by vn from the sequence initialized by seed_init.
- `P_INTEREDGE_HOLD`: The latched decision holds between rising CLK events even if VINP or VINN changes.
- `P_DELAY_AND_SMOOTHING`: DOUT applies td delay and tr transition smoothing after each latch event.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `latched_comparator_delay.va`.
Do not add or omit artifacts.
