# ADC Static Linearity Monitor

Implement one Verilog-A source file named `adc_static_linearity_monitor.va`.

## Public Interface

```verilog
module adc_static_linearity_monitor(vsample, vin, d2, d1, d0, maxerr);
```

All ports are electrical. `vsample` is the measurement strobe. `vin` is the
swept analog input. `d2` is the MSB and `d0` is the LSB of the observed ADC
output word. `maxerr` is an analog metric output.

## Public Parameter Contract

- `vref = 1.0 V`: ADC full-scale reference used for the ideal three-bit code.
- `vth = 0.45 V`: threshold for the measurement strobe and observed output bits.
- `lsb_out = 1.0 V`: output scale for one code of accumulated error.
- `tr = 20p`: metric output transition smoothing time.

## Required Behavior

Act as a sampled static-linearity measurement monitor for a three-bit ADC sweep.
On each rising crossing of `vsample` through `vth`, clip `vin` to the
0-to-`vref` range and compute the ideal bin-floor three-bit code. Decode the
observed `d2..d0` word using `vth`, compute the absolute code error in LSBs, and
retain the maximum sampled error seen so far during the run. Drive `maxerr` to
that retained maximum multiplied by `lsb_out`.

## Modeling Constraints

Use voltage-domain event-driven Verilog-A only. Update the metric only on the
measurement strobe and preserve the accumulated maximum instead of reporting only
the latest sample error. Do not hard-code testbench sample times, private checker
vectors, current contributions, `ddt()`, or `idt()`.
