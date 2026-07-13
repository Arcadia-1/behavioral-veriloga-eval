# Baseband AGC and Filter Chain Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `agc_chain_top.va`: `agc_chain_top`
- `level_meter.va`: `level_meter`
- `gain_controller.va`: `gain_controller`
- `vga_stage.va`: `vga_stage`
- `filter_stage.va`: `filter_stage`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_CLEAR`: Reset or disabled operation restores gain code 4, clears metrics and flags, and drives vout to vcm.
- `P_LEVEL_GAIN_CONTROL`: Each enabled rising clock samples the input magnitude and moves the bounded gain code toward the target deadband.
- `P_VGA_FILTER_RESPONSE`: The VGA applies gain_min plus gain_lsb times code and the sampled filter moves by alpha toward that VGA result.
- `P_CLIP_AND_SETTLE`: clip_flag reports an unclamped filter excursion beyond the rails and settled asserts only after three consecutive in-tolerance updates.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `agc_chain_top.va`, `level_meter.va`, `gain_controller.va`, `vga_stage.va`, `filter_stage.va`.
Every supplied `.va` file is editable; do not add or omit files.
