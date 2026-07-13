# Bang-bang CDR Loop Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `cdr_top.va`: `cdr_top`
- `bbpd.va`: `bbpd`
- `loop_filter_code.va`: `loop_filter_code`
- `phase_rotator.va`: `phase_rotator`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_DISABLE_CLEAR`: Reset or low enable restores phase_center and clears detector, lock, and recovered-clock state.
- `P_BANGBANG_DECISION`: Each data edge is classified against the nearest recovered-clock edge as early, late, or coincident.
- `P_PHASE_CODE_UPDATE`: Late and early decisions move the clamped phase code in opposite declared directions.
- `P_PHASE_ROTATION`: Recovered-clock edges preserve the reference-clock waveform with phase-code-proportional delay.
- `P_LOCK_QUALIFICATION`: Lock requires four in-window decisions and drops after two consecutive out-of-window decisions.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `cdr_top.va`, `bbpd.va`, `loop_filter_code.va`, `phase_rotator.va`.
Every supplied `.va` file is editable; do not add or omit files.
