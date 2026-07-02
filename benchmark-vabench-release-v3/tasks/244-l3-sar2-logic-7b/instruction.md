# L3 SAR2 Logic 7b

Implement `l3_sar2_logic_7b.va` as a voltage-domain SAR controller whose
comparator outputs encode active-low decisions.

## Public Interface

Use this module signature:

```verilog
module l3_sar2_logic_7b(
    clk, dp, dn, cmpck,
    do0, do1, do2, do3, do4, do5, do6,
    sp1, sp2, sp3, sp4, sp5, sp6,
    sn1, sn2, sn3, sn4, sn5, sn6
);
```

All ports are electrical. `clk` starts and resets the conversion, `dp` and `dn`
are active-low comparator decision pulses, `cmpck` requests comparator activity,
`do0..do6` are the final code bits, and `sp1..sp6`/`sn1..sn6` are the positive
and negative capacitor-selection controls.

## Public Parameter Contract

- `vdd`: high output level, default `0.9`.
- `vth`: logic threshold, default `0.45`.
- `tr`: transition time for driven outputs, default `20p`.

## Functional Contract

On a falling `clk` edge, reset the conversion state and clear final code bits.
On a rising `clk` edge, start the MSB-to-LSB SAR sequence and assert `cmpck`.
Each falling `dp` or `dn` edge records one active-low comparator decision:
`dn` falling selects the current bit high, while `dp` falling selects it low.
After the comparator outputs recover high, advance to the next bit and assert
`cmpck` for the next comparison. After the final bit decision, publish
`do6..do0` and leave `cmpck` low. The `sp`/`sn` controls should reflect the
latched decisions for bits 6 down to 1.

## Modeling Constraints

Use pure voltage-domain event-driven Verilog-A. Do not hard-code public
testbench edge times, private waveform names, or checker-only vectors.
