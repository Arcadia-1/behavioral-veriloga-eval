# Voltage Match Window

## Task Contract
Implement `voltage_match_window.va`, an analog voltage-coincidence detector for calibration, lock-detect, or monitor flows.

## Public Verilog-A Interface
Declare module `voltage_match_window(vin1, vin2, vout)` with scalar electrical ports. `vin1` and `vin2` are analog input voltages, and `vout` is a rail-coded match indicator.

## Public Parameter Contract
Provide overrideable public parameters:

- `match_tol = 0.05 V from [0:inf)`: maximum allowed absolute input difference for a match.
- `vh = 0.9 V`: match output level.
- `tr = 20 ps from [0:inf)`: output transition smoothing time.

The output low level is `0 V`.

## Required Behavior
Compare the analog voltage difference directly. Drive `vout` near `vh` when `abs(V(vin1) - V(vin2)) <= match_tol`; otherwise drive it near `0 V`. The decision should be deterministic and memoryless, with a smoothed voltage transition on the output.

## Modeling Constraints
Use deterministic voltage-domain Verilog-A and voltage contributions only. Do not emit a testbench, checker logic, out-of-band test hooks, hard-code testbench sample points, use current contributions, transistor-level devices, `ddt()`, `idt()`, or simulator side channels.

## Output Contract
Return exactly one source artifact named `voltage_match_window.va`.
