# 3-tap FFE Transmitter Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `ffe_tx_3tap.va`: `ffe_tx_3tap`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_CLEARS_SYMBOL_HISTORY_AND_DRIVES`: Reset clears symbol history and drives all outputs to common mode.
- `P_ON_EACH_RISING_CLK_SAMPLE_DATA`: On each rising `clk`, sample `data` as +1 for high and -1 for low.
- `P_DRIVE_MAIN_DBG_PRE_DBG_AND`: Drive `main_dbg`, `pre_dbg`, and `post_dbg` as voltage-coded per-tap contributions around common mode.
- `P_VOUT_IS_THE_CLIPPED_SUM_OF`: `vout` is the clipped sum of the current main contribution, previous-symbol pre contribution, and older-symbol post contribution.
- `P_HIGHER_TAP_CONTROL_CODES_MUST_INCREASE`: Higher tap-control codes must increase the corresponding contribution magnitude.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `ffe_tx_3tap.va`.
Every supplied `.va` file is editable; do not add or omit files.
