# Bandgap Startup and Trim System

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `bandgap_trim_top.va`: `bandgap_trim_top`
- `startup_detector.va`: `startup_detector`
- `ptat_ctat_core.va`: `ptat_ctat_core`
- `trim_controller.va`: `trim_controller`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_RESET_BROWNOUT_CLEAR`: On reset or brownout below POR, clear trim code, ready, error metric, and drive vref low.
- `P_POR_STARTUP`: Enable the reference only after vdd_sense remains above vpor for two consecutive rising clock edges.
- `P_CORE_REFERENCE`: Generate a behavioral PTAT/CTAT reference metric from temp_proxy around vref_nom.
- `P_TRIM_SEARCH`: When trim_req is high, update the 4-bit trim code once per rising clock edge to reduce reference error.
- `P_READY_QUALIFICATION`: Assert ready only after three consecutive enabled updates with error magnitude within ready_tol.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `bandgap_trim_top.va`, `startup_detector.va`, `ptat_ctat_core.va`, `trim_controller.va`.
Do not add or omit artifacts.
