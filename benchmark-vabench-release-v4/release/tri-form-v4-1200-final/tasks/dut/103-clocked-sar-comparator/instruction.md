# Clocked SAR Comparator

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `clocked_sar_comparator.va`: `clocked_sar_comparator`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIAL_PRECHARGE`: Both decision outputs initialize high at vdd.
- `P_FALLING_EDGE_PRECHARGE`: Each falling CMPCK crossing through vdd/2 resets both DCMPN and DCMPP high.
- `P_POSITIVE_DIFFERENTIAL_DECISION`: On a rising CMPCK crossing with VINP greater than VINN, DCMPP is high and DCMPN is low.
- `P_NEGATIVE_DIFFERENTIAL_DECISION`: On a rising CMPCK crossing with VINP less than VINN, DCMPN is high and DCMPP is low.
- `P_EQUAL_INPUT_DECISION`: On a rising CMPCK crossing with equal differential inputs, both decision outputs become low.
- `P_LATCHED_HOLD_AND_TIMING`: The precharged or decided state holds between clock events and output changes use td_cmp delay and tr smoothing.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `clocked_sar_comparator.va`.
Do not add or omit artifacts.
