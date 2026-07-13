# Voltage Match Window Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `voltage_match_window.va`: `voltage_match_window`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_COMPARE_THE_ANALOG_VOLTAGE_DIFFERENCE_DIRECTLY`: Compare the analog voltage difference directly. Drive `vout` near `vh` when `abs(V(vin1) - V(vin2)) <= match_tol`; otherwise drive it near `0 V`. The decision should be deterministic and memoryless, with a smoothed voltage transition on the output.
- `P_MATCH_TOL_0_05_V_FROM`: `match_tol = 0.05 V from [0:inf)`: maximum allowed absolute input difference for a match.
- `P_VH_0_9_V_MATCH_OUTPUT`: `vh = 0.9 V`: match output level.
- `P_TR_20_PS_FROM_0_INF`: `tr = 20 ps from [0:inf)`: output transition smoothing time.
- `P_MATCH_TOL_0_05_V_FROM_2`: - `match_tol = 0.05 V from [0:inf)`: maximum allowed absolute input difference for a match. - `vh = 0.9 V`: match output level. - `tr = 20 ps from [0:inf)`: output transition smoothing time.
- `P_USE_DETERMINISTIC_VOLTAGE_DOMAIN_VERILOG_A`: Use deterministic voltage-domain Verilog-A and voltage contributions only. Do not emit a testbench, checker logic, out-of-band test hooks, hard-code testbench sample points, use current contributions, transistor-level devices, `ddt()`, `idt()`, or simulator side channels.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `voltage_match_window.va`.
Every supplied `.va` file is editable; do not add or omit files.
