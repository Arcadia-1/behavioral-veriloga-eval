# SAR CDAC Residue

## Task Contract

Implement a scalar-port SAR CDAC residue update model.

- Form: `dut`
- Level: `L1`
- Category: data-converter support primitive
- Target artifact: `sar_cdac_residue.va`

## Form-Specific Requirements

Return only the DUT source file. Do not generate a simulation harness, validation script, waveform
postprocessor, or companion support module.

## Public Verilog-A Interface

`sar_cdac_residue.va` must declare:

```verilog
module sar_cdac_residue(VIN, CLK, S6, S5, S4, S3, S2, S1, VRES);
input VIN, CLK, S6, S5, S4, S3, S2, S1;
output VRES;
electrical VIN, CLK, S6, S5, S4, S3, S2, S1, VRES;
```

## Public Parameter Contract

- `vdd = 0.9`: control logic high level; switching threshold is `vdd/2`.
- `vrefp = 0.9`, `vrefn = 0`: CDAC reference endpoints. The full-scale span
  is `vrefp - vrefn`.

## Required Behavior

At `initial_step` and on each rising `CLK` threshold crossing, sample `VIN` into
the residue state. Then update the residue state from the SAR control inputs:

- falling `S6`: add `1/2` of the reference span;
- rising `S5`: subtract `1/4` of the reference span;
- rising `S4`: subtract `1/8` of the reference span;
- rising `S3`: subtract `1/16` of the reference span;
- rising `S2`: subtract `1/32` of the reference span;
- rising `S1`: subtract `1/64` of the reference span.

Drive `VRES` with a transition-shaped voltage contribution from the current
residue state.

## Modeling Constraints

Use voltage-domain event updates. Do not reinterpret the scalar control ports as
a packed bus, change the bit weights, change the event directions, or hard-code
testbench edge times.

## Output Contract

Return exactly one source artifact named `sar_cdac_residue.va`.
