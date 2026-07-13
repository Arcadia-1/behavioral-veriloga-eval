# Clocked Comparator Dual Output Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `clocked_comparator_dual_output.va`: `clocked_comparator_dual_output`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_INITIALIZE_BOTH_DECISION_OUTPUTS_LOW`: Initialize both decision outputs low.
- `P_WHENEVER_CLK_FALLS_THROUGH_VDD_2`: Whenever `clk` falls through `vdd/2`, reset both outputs low.
- `P_WHENEVER_CLK_RISES_THROUGH_VDD_2`: Whenever `clk` rises through `vdd/2`, latch a differential decision.
- `P_DRIVE_OUTP_HIGH_AND_OUTN_LOW`: Drive `outp` high and `outn` low for `vinp > vinn`.
- `P_DRIVE_OUTN_HIGH_AND_OUTP_LOW`: Drive `outn` high and `outp` low for `vinp < vinn`.
- `P_DRIVE_BOTH_OUTPUTS_LOW_FOR_AN`: Drive both outputs low for an equal-input decision.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `clocked_comparator_dual_output.va`.
Every supplied `.va` file is editable; do not add or omit files.
