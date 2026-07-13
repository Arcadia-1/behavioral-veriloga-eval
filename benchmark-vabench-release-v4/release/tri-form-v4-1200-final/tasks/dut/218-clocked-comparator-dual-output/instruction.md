# Clocked Comparator Dual Output

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `clocked_comparator_dual_output.va`: `clocked_comparator_dual_output`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_INITIALIZE_BOTH_DECISION_OUTPUTS_LOW`: Initialize both decision outputs low.
- `P_WHENEVER_CLK_FALLS_THROUGH_VDD_2`: Whenever `clk` falls through `vdd/2`, reset both outputs low.
- `P_WHENEVER_CLK_RISES_THROUGH_VDD_2`: Whenever `clk` rises through `vdd/2`, latch a differential decision.
- `P_DRIVE_OUTP_HIGH_AND_OUTN_LOW`: Drive `outp` high and `outn` low for `vinp > vinn`.
- `P_DRIVE_OUTN_HIGH_AND_OUTP_LOW`: Drive `outn` high and `outp` low for `vinp < vinn`.
- `P_DRIVE_BOTH_OUTPUTS_LOW_FOR_AN`: Drive both outputs low for an equal-input decision.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `clocked_comparator_dual_output.va`.
Do not add or omit artifacts.
