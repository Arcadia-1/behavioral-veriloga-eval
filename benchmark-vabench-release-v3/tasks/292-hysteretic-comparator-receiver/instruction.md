# Hysteretic Comparator Receiver

## Task Contract
Implement `hysteretic_comparator_receiver.va`, a voltage-domain comparator receiver with input hysteresis, propagation delay, and rail-coded output. This follows the Cadence-style comparator modeling pattern of using an offset and hysteresis width to form upper and lower switching thresholds.

## Public Verilog-A Interface
Declare module `hysteretic_comparator_receiver(inp, inm, out)` with scalar electrical ports. `inp` and `inm` form the differential input, and `out` is the voltage-coded receiver output.

## Public Parameter Contract
Provide overrideable public parameters:

- `vout_high = 0.9 V`: high output rail.
- `vout_low = 0.0 V`: low output rail.
- `offset = 0.0 V`: input-referred switching offset.
- `vhys = 40 mV from [0:inf)`: total hysteresis width.
- `td = 400 ps from [0:inf)`: propagation delay from a qualifying threshold crossing to the output state change.
- `tr = 80 ps from [0:inf)`: output transition smoothing time.

## Required Behavior
Define `upper_th = offset + vhys/2` and `lower_th = offset - vhys/2`. On initialization, set the output state high if `V(inp,inm)` is at or above the upper threshold; otherwise set it low. After initialization, switch high only on a rising crossing of `upper_th`, switch low only on a falling crossing of `lower_th`, and hold the previous state inside the hysteresis band. Drive `out` to the selected rail with delay `td` and transition time `tr`.

## Modeling Constraints
Use voltage contributions and event-driven Verilog-A threshold crossings. Do not emit a testbench, checker logic, out-of-band test hooks, hard-code waveform sample points, use current contributions, transistor-level devices, `ddt()`, `idt()`, or simulator side channels.

## Output Contract
Return exactly one source artifact named `hysteretic_comparator_receiver.va`.
