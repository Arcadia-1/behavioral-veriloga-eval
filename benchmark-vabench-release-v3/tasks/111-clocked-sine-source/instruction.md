# Clocked Sine Source

Implement `vin_src.va` in Verilog-A.

## Public Interface

Declare module `vin_src(CLK, RST_N, VOUT_P, VOUT_N)` with scalar electrical
voltage-domain ports. `CLK` and `RST_N` are voltage-coded control inputs, and
`VOUT_P` and `VOUT_N` are the differential source outputs.

## Public Parameter Contract

- `vdd`: output supply and common-mode parameter, default `0.9`.
- `vth`: logic threshold for `CLK` and `RST_N`, default `0.45`.
- `ampl`: sine amplitude in volts, default `0.15`.
- `freq`: sine frequency in Hz, default `300e3`.
- `sigma`: Gaussian perturbation scale in volts, default `0.01`.
- `SEED`: deterministic random seed, default `0`.

## Functional Contract

- Initialize both outputs to `vdd / 2`.
- On each rising `CLK` edge while `RST_N > vth`, update `VOUT_P` to a sampled
  sine value around `vdd / 2` plus deterministic Gaussian perturbation.
- Hold `VOUT_P` between clock edges and while reset is not released.
- Keep `VOUT_N` at `vdd / 2` as the complementary reference side.
- Drive both outputs with smoothed voltage-domain transitions.

## Modeling Constraints

Return only `vin_src.va`; companion files used by the validation scenario are
supplied separately. Do not emit a Spectre testbench, checker logic, private
test hooks, or simulator-private side channels. Use voltage-domain,
event-driven Verilog-A; do not use transistor-level devices, current
contributions, `ddt()`, or `idt()`.
