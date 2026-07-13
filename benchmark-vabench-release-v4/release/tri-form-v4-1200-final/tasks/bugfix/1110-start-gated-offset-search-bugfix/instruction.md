# Start Gated Offset Search Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `start_gated_offset_search.va`: `start_gated_offset_search`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_DISABLED_COMMON_MODE`: While START is below vstart_th, VINP and VINN both equal vcm and the internal search state is reset.
- `P_START_REINITIALIZATION`: Each rising START crossing through vstart_th reinitializes differential value to zero, step to 20 mV, and remembered direction high.
- `P_FALLING_CLOCK_UPDATES`: While START is high, search updates occur only on falling CLK crossings through vdd/2.
- `P_DECISION_DIRECTED_STEP`: At each enabled update, VOUT above vdd/2 moves the differential value positive and VOUT at or below vdd/2 moves it negative.
- `P_REVERSAL_STEP_HALVING`: When the newly sampled decision direction differs from the remembered direction, the current step is halved before applying the move.
- `P_COMMON_MODE_AND_DIFFERENTIAL`: During search, the average of VINP and VINN remains vcm and their difference equals the accumulated differential search value.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `start_gated_offset_search.va`.
Every supplied `.va` file is editable; do not add or omit files.
