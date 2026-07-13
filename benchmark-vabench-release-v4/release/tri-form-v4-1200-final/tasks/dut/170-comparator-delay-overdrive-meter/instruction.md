# Comparator Delay Overdrive Meter

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `comparator_delay_overdrive_meter.va`: `comparator_delay_overdrive_meter`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CLOCK_ARMED_MEASUREMENT`: Each rising `clk` threshold crossing stores the launch time, captures absolute differential overdrive, and arms exactly one pending measurement.
- `P_DECISION_DELAY_CAPTURE`: The first qualifying `outp` or `outn` decision edge while armed reports the elapsed clock-to-decision delay in `delay_ps`.
- `P_ABSOLUTE_OVERDRIVE_METRIC`: `overdrive_mv` reports the absolute input differential magnitude at launch time.
- `P_POLARITY_AND_VALID_FLAG`: `polarity` reports the winning output decision direction and `valid` asserts only for a completed armed measurement.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `comparator_delay_overdrive_meter.va`.
Do not add or omit artifacts.
