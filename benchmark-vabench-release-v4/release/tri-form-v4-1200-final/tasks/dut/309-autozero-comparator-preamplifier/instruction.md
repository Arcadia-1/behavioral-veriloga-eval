# Auto-zero Comparator Preamplifier

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `autozero_comparator_preamplifier_top.va`: `autozero_comparator_preamplifier_top`
- `offset_store_cell.va`: `offset_store_cell`
- `clocked_comparator_core.va`: `clocked_comparator_core`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_CLEAR_STORED_OFFSET_DECISION`: On reset, clear stored offset, `decision`, and `ready`.
- `P_DURING_AN_AUTO_ZERO_CLOCK_UPDATE`: During an auto-zero clock update with `az_en` high, store the apparent differential offset between `vinp` and `vinn`.
- `P_DURING_AN_EVALUATION_CLOCK_UPDATE_WITH`: During an evaluation clock update with `eval_en` high, subtract the stored offset from the live differential input.
- `P_DRIVE_DECISION_HIGH_FOR_CORRECTED_NONNEGATIVE`: Drive `decision` high for corrected nonnegative differential input and low otherwise.
- `P_EXPOSE_STORED_OFFSET_ON_OFFSET_STORE`: Expose stored offset on `offset_store` and assert `ready` after at least one auto-zero update.
- `P_USE_ONLY_VOLTAGE_DOMAIN_BEHAVIORAL_STATE`: Use only voltage-domain behavioral state and voltage contributions on public electrical outputs.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `autozero_comparator_preamplifier_top.va`, `offset_store_cell.va`, `clocked_comparator_core.va`.
Do not add or omit artifacts.
