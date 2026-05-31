Write a Verilog-A module named `flash_adc_3b` and one EVAS-compatible Spectre testbench for a 3-bit flash ADC mini-array.

Create a pure voltage-domain 3-bit flash ADC mini-array. The DUT must expose
the seven comparator decisions as a thermometer vector and encode that vector
into a 3-bit binary output after clocked sampling.

## DUT Contract

- Module name: `flash_adc_3b`
- Ports, all `electrical`, exactly in this order: `vdd`, `vss`, `vin`, `clk`, `cmp0`, `cmp1`, `cmp2`, `cmp3`, `cmp4`, `cmp5`, `cmp6`, `dout2`, `dout1`, `dout0`
- Parameters:
  - `vrefp` real, default `0.9`
  - `vrefn` real, default `0.0`
  - `vth` real, default `0.45`
  - `tedge` real, default `100p`
- Behavior:
  - Full-scale range is `vrefn` to `vrefp`, divided into 8 equal bins.
  - On each rising `clk` edge, compare `V(vin)` against the seven thresholds
    `vrefn + k*(vrefp-vrefn)/8` for `k=1..7`.
  - Drive `cmp0` through `cmp6` as the latched threshold-comparator decisions,
    where `cmp0` is the 1-LSB threshold and `cmp6` is the 7-LSB threshold.
  - The comparator outputs must form a thermometer prefix: higher thresholds
    cannot be high unless all lower thresholds are high.
  - Encode the number of high comparator outputs into `dout2:dout1:dout0`,
    with `dout2` as MSB and `dout0` as LSB.
  - Output HIGH should be `V(vdd)` and output LOW should be `V(vss)`.
  - Use `@(cross(V(clk) - vth, +1))` and `transition(...)`.

## Testbench Contract

- Use a 0.9 V supply and 0 V reference.
- Drive `vin` through the midpoint of each of the 8 quantization bins, using
  stable windows before each clock edge.
- Drive `clk` so the checker can sample one stable conversion for every code
  from `0` through `7`.
- Instantiate the DUT by positional ports.
- Save these exact scalar names: `vin`, `clk`, `cmp0`, `cmp1`, `cmp2`, `cmp3`, `cmp4`, `cmp5`, `cmp6`, `dout2`, `dout1`, `dout0`.
- Include the generated DUT file `flash_adc_3b.va`.

Return exactly two files: `flash_adc_3b.va` and `tb_flash_adc_3b_ref.scs`.
