# Offset-calibrated Comparator System Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `calibrated_comparator_top.va`: `calibrated_comparator_top`
- `comparator_core.va`: `comparator_core`
- `offset_dac.va`: `offset_dac`
- `calibration_fsm.va`: `calibration_fsm`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_CAL_RESET_CLEAR`: Reset clears offset code, decision, ready, and threshold_dbg.
- `P_CAL_CODE_UPDATE`: Each enabled rising clock updates and clamps the offset code in the direction selected by cal_ref.
- `P_CAL_OFFSET_DAC`: threshold_dbg equals signed code minus eight times offset_lsb outside reset.
- `P_CAL_READY_QUALIFICATION`: ready asserts after four updates in one calibration window and the code holds while cal_en is low.
- `P_CAL_COMPARATOR_DECISION`: decision reflects the sign of vinp minus vinn plus threshold_dbg and is low in reset.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `calibrated_comparator_top.va`, `comparator_core.va`, `offset_dac.va`, `calibration_fsm.va`.
Every supplied `.va` file is editable; do not add or omit files.
