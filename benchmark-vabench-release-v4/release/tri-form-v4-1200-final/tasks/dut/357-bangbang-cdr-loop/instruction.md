# Bang-bang CDR Loop

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `cdr_top.va`: `cdr_top`
- `bbpd.va`: `bbpd`
- `loop_filter_code.va`: `loop_filter_code`
- `phase_rotator.va`: `phase_rotator`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_DISABLE_CLEAR`: Reset or low enable restores phase_center and clears detector, lock, and recovered-clock state.
- `P_BANGBANG_DECISION`: Each data edge is classified against the nearest recovered-clock edge as early, late, or coincident.
- `P_PHASE_CODE_UPDATE`: Late and early decisions move the clamped phase code in opposite declared directions.
- `P_PHASE_ROTATION`: Recovered-clock edges preserve the reference-clock waveform with phase-code-proportional delay.
- `P_LOCK_QUALIFICATION`: Lock requires four in-window decisions and drops after two consecutive out-of-window decisions.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `cdr_top.va`, `bbpd.va`, `loop_filter_code.va`, `phase_rotator.va`.
Do not add or omit artifacts.
