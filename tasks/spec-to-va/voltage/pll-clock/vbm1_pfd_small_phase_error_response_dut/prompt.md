# Task: vbm1_pfd_small_phase_error_response_dut

Write a pure voltage-domain Verilog-A DUT for a phase-frequency detector that
responds correctly to small REF/DIV phase errors.

Return exactly one complete Verilog-A file named `pfd_updn.va`.

## Module Contract

Implement this module declaration and port order:

```verilog
module pfd_updn(VDD, VSS, REF, DIV, UP, DN);
```

All ports are `electrical`. `VDD` and `VSS` are supply rails, `REF` and `DIV`
are input clocks, and `UP` and `DN` are output pulses. Public stimulus uses
`VDD=0.9 V`, `VSS=0 V`, and small REF/DIV phase offsets.

## Required Behavior

- A rising edge on `REF` asserts `UP`.
- A rising edge on `DIV` asserts `DN`.
- When both internal UP and DN states have arrived, reset both outputs back to
  low so overlap is short and bounded.
- For a small REF-leading-DIV phase error, generate repeated short `UP` pulses
  and no sustained `DN` pulse train.
- Drive output HIGH from `VDD` and LOW from `VSS`, read dynamically.
- Stay in the pure voltage-domain behavioral subset. Do not use current
  contributions, `ddt`, or `idt`.

## Public Evaluation Observables

The public checker saves `REF`, `DIV`, `UP`, and `DN`. It checks that small
phase-error stimulus produces bounded `UP` pulse activity, that `DN` remains
low except for reset overlap transients, and that UP/DN overlap is not
sustained.
