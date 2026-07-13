# Bandgap Startup and Trim System Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `bandgap_trim_top.va`: `bandgap_trim_top`
- `startup_detector.va`: `startup_detector`
- `ptat_ctat_core.va`: `ptat_ctat_core`
- `trim_controller.va`: `trim_controller`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_RESET_BROWNOUT_CLEAR`: On reset or brownout below POR, clear trim code, ready, error metric, and drive vref low.
- `P_POR_STARTUP`: Enable the reference only after vdd_sense remains above vpor for two consecutive rising clock edges.
- `P_CORE_REFERENCE`: Generate a behavioral PTAT/CTAT reference metric from temp_proxy around vref_nom.
- `P_TRIM_SEARCH`: When trim_req is high, update the 4-bit trim code once per rising clock edge to reduce reference error.
- `P_READY_QUALIFICATION`: Assert ready only after three consecutive enabled updates with error magnitude within ready_tol.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `bandgap_trim_top.va`, `startup_detector.va`, `ptat_ctat_core.va`, `trim_controller.va`.
Every supplied `.va` file is editable; do not add or omit files.
