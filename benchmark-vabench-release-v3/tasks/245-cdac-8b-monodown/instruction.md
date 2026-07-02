# CDAC 8b Monodown

Implement `cdac_8b_monodown.va` as an 8-bit SAR CDAC residue model using
monotonic downward switching.

## Public Interface

Use this module signature:

```verilog
module cdac_8b_monodown(vin, clks, dctrl1, dctrl2, dctrl3, dctrl4, dctrl5, dctrl6, dctrl7, vres);
```

All ports are electrical. `vin` is the sampled input, `clks` is the sampling
clock, `dctrl1..dctrl7` are decision/control edges, and `vres` is the residue
output.

## Public Parameter Contract

- `vth`: logic threshold, default `0.5`.
- `tr`: output transition time, default `20p`.
- The normalized CDAC reference span is 1 V.

## Functional Contract

On each falling `clks` crossing, sample `vin` into the held residue. On rising
control crossings, subtract the corresponding binary-weighted fraction from the
held residue:

- `dctrl7`: subtract `1/2`
- `dctrl6`: subtract `1/4`
- `dctrl5`: subtract `1/8`
- `dctrl4`: subtract `1/16`
- `dctrl3`: subtract `1/32`
- `dctrl2`: subtract `1/64`
- `dctrl1`: subtract `1/128`

Between sampling and control events, hold the current residue value.

## Modeling Constraints

Use pure voltage-domain event-driven Verilog-A. Do not hard-code visible
stimulus timing, private sample points, or checker-only values.
