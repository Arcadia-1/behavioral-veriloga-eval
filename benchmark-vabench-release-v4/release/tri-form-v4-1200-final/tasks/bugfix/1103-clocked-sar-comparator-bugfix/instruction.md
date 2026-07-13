# Clocked SAR Comparator Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `clocked_sar_comparator.va`: `clocked_sar_comparator`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_PRECHARGE`: Both decision outputs initialize high at vdd.
- `P_FALLING_EDGE_PRECHARGE`: Each falling CMPCK crossing through vdd/2 resets both DCMPN and DCMPP high.
- `P_POSITIVE_DIFFERENTIAL_DECISION`: On a rising CMPCK crossing with VINP greater than VINN, DCMPP is high and DCMPN is low.
- `P_NEGATIVE_DIFFERENTIAL_DECISION`: On a rising CMPCK crossing with VINP less than VINN, DCMPN is high and DCMPP is low.
- `P_EQUAL_INPUT_DECISION`: On a rising CMPCK crossing with equal differential inputs, both decision outputs become low.
- `P_LATCHED_HOLD_AND_TIMING`: The precharged or decided state holds between clock events and output changes use td_cmp delay and tr smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `clocked_sar_comparator.va`.
Every supplied `.va` file is editable; do not add or omit files.
