# Offset-calibrated Comparator System

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `calibrated_comparator_top.va`: `calibrated_comparator_top`
- `comparator_core.va`: `comparator_core`
- `offset_dac.va`: `offset_dac`
- `calibration_fsm.va`: `calibration_fsm`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_CAL_RESET_CLEAR`: Reset clears offset code, decision, ready, and threshold_dbg.
- `P_CAL_CODE_UPDATE`: Each enabled rising clock updates and clamps the offset code in the direction selected by cal_ref.
- `P_CAL_OFFSET_DAC`: threshold_dbg equals signed code minus eight times offset_lsb outside reset.
- `P_CAL_READY_QUALIFICATION`: ready asserts after four updates in one calibration window and the code holds while cal_en is low.
- `P_CAL_COMPARATOR_DECISION`: decision reflects the sign of vinp minus vinn plus threshold_dbg and is low in reset.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `calibrated_comparator_top.va`, `comparator_core.va`, `offset_dac.va`, `calibration_fsm.va`.
Do not add or omit artifacts.
