# Fixed Gain Amplifier

Implement `gain_amp_fixed.va` in Verilog-A.

## Public Interface

Declare module `gain_amp_fixed(VIN_P, VIN_N, VOUT_P, VOUT_N)` with scalar
electrical voltage-domain ports. `VIN_P` and `VIN_N` are the differential
input, and `VOUT_P` and `VOUT_N` are the fixed-gain differential outputs.

## Public Parameter Contract

- `vdd`: output common-mode supply parameter, default `0.9`.
- `ACTUAL_GAIN`: differential voltage gain, default `8.64`.

## Functional Contract

- Compute the input differential voltage as `V(VIN_P, VIN_N)`.
- Drive the output differential voltage as
  `ACTUAL_GAIN * V(VIN_P, VIN_N)`.
- Center the output pair around `vdd / 2`:
  `VOUT_P = vdd / 2 + output_diff / 2` and
  `VOUT_N = vdd / 2 - output_diff / 2`.
- Keep the behavior deterministic and purely voltage-domain.

## Modeling Constraints

Return only `gain_amp_fixed.va`; companion files used by the validation
scenario are supplied separately. Do not emit a Spectre testbench, checker
logic, private test hooks, or simulator-private side channels. Use
voltage-domain Verilog-A voltage contributions only; do not use transistor-level
devices, current contributions, `ddt()`, or `idt()`.
