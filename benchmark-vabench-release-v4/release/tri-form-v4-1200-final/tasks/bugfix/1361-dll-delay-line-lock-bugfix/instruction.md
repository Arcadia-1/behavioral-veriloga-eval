# DLL Delay-line Lock Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `dll_top.va`: `dll_top`
- `phase_detector.va`: `phase_detector`
- `delay_line.va`: `delay_line`
- `lock_detector.va`: `lock_detector`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_CLEAR`: Reset or disabled operation restores delay_center, clears correction and lock outputs, cancels pending edges, and drives delayed_clk low.
- `P_DELAY_LINE_DERIVATION`: Each delayed-clock edge derives from the matching input-clock edge using the code selected for that edge; the output is not free-running.
- `P_PHASE_CORRECTION`: Completed ref/delayed comparisons request the correction direction that moves the delay code toward edge alignment and update the code once within 0 through 31.
- `P_LOCK_QUALIFICATION`: Lock asserts only after four consecutive comparisons within lock_window times unit_delay and clears after an out-of-window comparison.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `dll_top.va`, `phase_detector.va`, `delay_line.va`, `lock_detector.va`.
Every supplied `.va` file is editable; do not add or omit files.
