# PFD Up DN Logic

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `pfd_updn.va`: `pfd_updn`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_REF_SETS_UP`: A rising REF edge asserts UP, and falling REF edges do not set either output.
- `P_DIV_SETS_DN`: A rising DIV edge asserts DN, and falling DIV edges do not set either output.
- `P_RESET_RACE_CLEAR`: If a rising edge arrives while the opposite output state is already high, both UP and DN clear immediately for REF-leading and DIV-leading orderings.
- `P_NO_PERSISTENT_OVERLAP`: UP and DN are not intentionally held high together beyond finite transition smoothing overlap.
- `P_RAIL_REFERENCE`: UP and DN high levels track the local VDD rail and low levels track the local VSS rail.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `pfd_updn.va`.
Do not add or omit artifacts.
