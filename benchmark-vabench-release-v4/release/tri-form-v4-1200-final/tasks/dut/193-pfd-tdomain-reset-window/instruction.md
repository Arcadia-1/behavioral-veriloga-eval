# PFD Tdomain Reset Window

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `pfd_tdomain_reset_window.va`: `pfd_tdomain_reset_window`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_LEADING_EDGE_DIRECTION`: A leading `in1` edge asserts `up`, and a leading `in2` edge asserts `dn`.
- `P_RESET_OVERLAP_WINDOW`: After both inputs arrive, both outputs remain asserted for the `ton` reset-overlap window.
- `P_CLEAR_AFTER_RESET_WINDOW`: After the reset-overlap window, both `up` and `dn` clear before the next phase event.
- `P_PFD_OUTPUT_LEVELS`: `up` and `dn` use rail-referenced voltage-coded low/high levels.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `pfd_tdomain_reset_window.va`.
Do not add or omit artifacts.
