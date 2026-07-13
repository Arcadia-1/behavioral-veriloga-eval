# Clocked Comparator Reset Low Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `clocked_comparator_reset_low.va`: `clocked_comparator_reset_low`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIAL_RESET_LOW`: Both decision outputs initialize low.
- `P_FALLING_EDGE_RESET_LOW`: Each falling CMPCK crossing through vdd/2 resets both DCMPN and DCMPP low.
- `P_POSITIVE_DIFFERENTIAL_DECISION`: On a rising CMPCK crossing with VINP greater than VINN, DCMPP is high and DCMPN is low.
- `P_NEGATIVE_DIFFERENTIAL_DECISION`: On a rising CMPCK crossing with VINP less than VINN, DCMPN is high and DCMPP is low.
- `P_EQUAL_INPUT_RESET_STATE`: On a rising CMPCK crossing with equal inputs, both outputs remain low.
- `P_LATCHED_HOLD_AND_TIMING`: The reset or decided state holds between CMPCK events and output changes use td_cmp delay and tr smoothing.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `clocked_comparator_reset_low.va`.
Every supplied `.va` file is editable; do not add or omit files.
