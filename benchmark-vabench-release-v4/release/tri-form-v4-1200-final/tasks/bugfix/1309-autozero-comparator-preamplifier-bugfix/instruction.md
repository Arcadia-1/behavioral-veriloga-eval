# Auto-zero Comparator Preamplifier Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `autozero_comparator_preamplifier_top.va`: `autozero_comparator_preamplifier_top`
- `offset_store_cell.va`: `offset_store_cell`
- `clocked_comparator_core.va`: `clocked_comparator_core`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ON_RESET_CLEAR_STORED_OFFSET_DECISION`: On reset, clear stored offset, `decision`, and `ready`.
- `P_DURING_AN_AUTO_ZERO_CLOCK_UPDATE`: During an auto-zero clock update with `az_en` high, store the apparent differential offset between `vinp` and `vinn`.
- `P_DURING_AN_EVALUATION_CLOCK_UPDATE_WITH`: During an evaluation clock update with `eval_en` high, subtract the stored offset from the live differential input.
- `P_DRIVE_DECISION_HIGH_FOR_CORRECTED_NONNEGATIVE`: Drive `decision` high for corrected nonnegative differential input and low otherwise.
- `P_EXPOSE_STORED_OFFSET_ON_OFFSET_STORE`: Expose stored offset on `offset_store` and assert `ready` after at least one auto-zero update.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `autozero_comparator_preamplifier_top.va`, `offset_store_cell.va`, `clocked_comparator_core.va`.
Every supplied `.va` file is editable; do not add or omit files.
