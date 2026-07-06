# Dither Noise Like Deterministic Source

## Task Contract

Implement the requested Verilog-A artifact for `Dither Noise Like Deterministic Source`.
- Form: `dut`
- Level: `L1`
- Category: `stimulus_source_generators`
- Target artifact(s): `noise_gen_ref.va`

Implement `noise_gen_ref.va` in Verilog-A.

## Public Verilog-A Interface

Declare module `noise_gen` with positional ports `vin_i, vout_o`. Both ports
are electrical.

## Public Parameter Contract

- `sigma = 0.01 V`: perturbation amplitude/statistical scale before any
  testbench override.
- `dt = 0.5 ns`: sample interval before any testbench override.

## Required Behavior

Generate a sampled, zero-mean, noise-like deterministic perturbation and add it
to `V(vin_i)`. The output is piecewise constant between sample events:

```text
vout_o = V(vin_i) + sigma * sample
```

Use a periodic timer-driven sample-and-hold style, such as `@(timer(0, dt))`,
so the perturbation is updated once per sample interval rather than recomputed
at every analog evaluation point or sampled only once. The task models a
bounded dither/noise-like stimulus source for transient behavioral benches; it
does not require physical noise analysis.

## Modeling Constraints

Return only `noise_gen_ref.va`. Do not generate a Spectre testbench or validation harness
logic. Do not use current contributions, `ddt()`, `idt()`, transistor-level
devices, AC/noise analysis, or simulator-specific side channels.

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete source artifact named `noise_gen_ref.va`. Do not include explanatory prose outside the source artifact contents.
