# Tool 4bit SAR Signed DAC

Implement `tool_4bit_sar_signed_dac.va` as a sample-triggered signed SAR
reconstruction DAC for a SAR-style readout path.

## Public Interface

Use this module signature:

```verilog
module tool_4bit_sar_signed_dac(d0, d1, d2, d3, sh, aout);
```

All ports are electrical. `d0..d3` are voltage-coded decision bits, `sh` is the
sample trigger, and `aout` is the signed analog output.

## Public Parameter Contract

- `vth`: logic threshold, default `0.9`.
- `gain`: signed output scale, default `1.8/16`.
- `tr`: output transition time, default `1p`.

## Functional Contract

On each rising `sh` crossing, evaluate bits `d3..d0` with weights 8, 4, 2, and
1. A high bit contributes the positive weight and a low bit contributes the
negative weight. Drive `aout` to the signed weighted sum multiplied by `gain`
and hold it until the next sample trigger.

## Modeling Constraints

Use pure voltage-domain event-driven Verilog-A. Do not hard-code visible
stimulus timing, private sample points, or checker-only expected values.
