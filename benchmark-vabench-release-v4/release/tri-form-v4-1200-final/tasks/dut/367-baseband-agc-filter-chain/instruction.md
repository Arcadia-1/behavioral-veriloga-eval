# Baseband AGC and Filter Chain

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `agc_chain_top.va`: `agc_chain_top`
- `level_meter.va`: `level_meter`
- `gain_controller.va`: `gain_controller`
- `vga_stage.va`: `vga_stage`
- `filter_stage.va`: `filter_stage`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CLEAR`: Reset or disabled operation restores gain code 4, clears metrics and flags, and drives vout to vcm.
- `P_LEVEL_GAIN_CONTROL`: Each enabled rising clock samples the input magnitude and moves the bounded gain code toward the target deadband.
- `P_VGA_FILTER_RESPONSE`: The VGA applies gain_min plus gain_lsb times code and the sampled filter moves by alpha toward that VGA result.
- `P_CLIP_AND_SETTLE`: clip_flag reports an unclamped filter excursion beyond the rails and settled asserts only after three consecutive in-tolerance updates.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `agc_chain_top.va`, `level_meter.va`, `gain_controller.va`, `vga_stage.va`, `filter_stage.va`.
Do not add or omit artifacts.
