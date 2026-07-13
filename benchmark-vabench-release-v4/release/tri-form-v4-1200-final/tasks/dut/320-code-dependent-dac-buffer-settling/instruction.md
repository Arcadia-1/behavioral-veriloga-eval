# Code-dependent DAC Buffer Settling

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `code_dependent_dac_buffer_top.va`: `code_dependent_dac_buffer_top`
- `ideal_code_dac.va`: `ideal_code_dac`
- `settling_buffer_state.va`: `settling_buffer_state`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ON_RESET_OR_WHEN_DISABLED_CLEAR`: On reset or when disabled, drive `vout` to `vcm` and drive `target_dbg`, `settling_metric`, and `settled` to `vss`.
- `P_ON_EACH_ENABLED_RISING_CLK_EDGE`: Decode code 0..15 linearly from `vss` to `vdd`; on each enabled rising `clk` edge update the buffered output toward that target.
- `P_APPLY_A_CODE_DEPENDENT_SETTLING_STEP`: Apply a code-dependent settling step so large code jumps take more updates to settle.
- `P_EXPOSE_THE_CURRENT_TARGET_ON_TARGET`: Expose the current target on `target_dbg` and the remaining error on `settling_metric`.
- `P_ASSERT_SETTLED_AFTER_THE_REMAINING_ERROR`: Assert `settled` after the remaining error stays below `settle_tol` for two enabled updates.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `code_dependent_dac_buffer_top.va`, `ideal_code_dac.va`, `settling_buffer_state.va`.
Do not add or omit artifacts.
