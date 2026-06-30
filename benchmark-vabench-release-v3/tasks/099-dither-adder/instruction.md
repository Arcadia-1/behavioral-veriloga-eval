# Dither Adder

Implement `dither_adder.va` in Verilog-A.

## Public Interface

Declare module `dither_adder(VRES_P, VRES_N, DPN, VOUT_P, VOUT_N)` with scalar
electrical voltage-domain ports. `VRES_P` and `VRES_N` are the differential
input residual, `DPN` is a voltage-coded dither sign input, and `VOUT_P` and
`VOUT_N` are the dithered differential outputs.

## Public Parameter Contract

- `vdd`: harness compatibility supply parameter, default `0.9`.
- `vth`: dither sign threshold for `DPN`, default `0.45`.
- `DITHER_AMP`: differential dither amplitude in volts, default `0.014063`.

## Functional Contract

- Interpret `DPN > vth` as positive dither and `DPN <= vth` as negative
  dither.
- For positive dither, apply `+DITHER_AMP` to the differential output:
  `VOUT_P = VRES_P + DITHER_AMP / 2` and
  `VOUT_N = VRES_N - DITHER_AMP / 2`.
- For negative dither, apply `-DITHER_AMP` to the differential output:
  `VOUT_P = VRES_P - DITHER_AMP / 2` and
  `VOUT_N = VRES_N + DITHER_AMP / 2`.
- Preserve the input common-mode while adding only the signed differential
  dither term.

## Modeling Constraints

Return only `dither_adder.va`; companion files used by the validation scenario
are supplied separately. Do not emit a Spectre testbench, checker logic,
private test hooks, or simulator-private side channels. Use voltage-domain
Verilog-A voltage contributions only; do not use transistor-level devices,
current contributions, `ddt()`, or `idt()`.
