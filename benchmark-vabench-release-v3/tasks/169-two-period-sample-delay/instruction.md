# Two Period Sample Delay

## Task Contract

Implement a clocked analog sample-delay element.

- Form: `dut`
- Level: `L1`
- Category: sampled-data analog utility
- Target artifact: `two_period_sample_delay.va`

## Form-Specific Requirements

Return only the DUT source file. Do not generate a simulation harness, validation script, waveform
postprocessor, or companion support module.

## Public Verilog-A Interface

`two_period_sample_delay.va` must declare:

```verilog
module two_period_sample_delay(update, ain, aout);
input update, ain;
output aout;
electrical update, ain, aout;
```

## Public Parameter Contract

- `vth = 0.5`: rising update-edge threshold in volts.
- `init = 0.0`: output and stored-sample value before valid delayed samples
  are available.
- `tr = 50p`: output transition rise/fall time.

## Required Behavior

Initialize the stored samples and output to `init`. On each rising threshold
crossing of `update`, drive the output state with the sample captured on the
previous update edge, then capture the current `V(ain)` for use on the next
update edge.

Before a previous update sample exists, the output remains at `init`.

## Modeling Constraints

Use voltage-domain sample-and-hold state and a transition-shaped output. Do not
track `ain` continuously, sample on falling edges, skip the initial value, or
hard-code testbench edge times.

## Output Contract

Return exactly one source artifact named `two_period_sample_delay.va`.
