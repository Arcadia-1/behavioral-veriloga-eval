Write a Verilog-A module named `simultaneous_event_order_ref`.

# Task: simultaneous_event_order_smoke

## Objective

Write a Verilog-A model where an absolute timer event and a `cross()` event happen at the same nominal times, and the final plateau level reveals the execution order.

Public behavior requirements:
- The Spectre testbench should drive `VDD=0.9 V`, `VSS=0 V`, and a `ref` pulse train whose rising edges occur at 10 ns, 30 ns, 50 ns, and 70 ns.
- The DUT should schedule absolute timer events on the same 10 ns + 20 ns grid.
- After each same-time timer/cross event pair, `out` should settle to approximately 20%, 40%, 60%, and 80% of `VDD`, respectively.
- Use voltage-domain contributions and smooth transitions; do not use current-domain branch contributions.

Ports:
- `VDD`: inout electrical
- `VSS`: inout electrical
- `ref`: input electrical
- `out`: output electrical

## Output Contract (MANDATORY)

- Return exactly two fenced code blocks:
  - first block: Verilog-A DUT (` ```verilog-a ... ``` `)
  - second block: Spectre testbench (` ```spectre ... ``` `)
- The Spectre testbench must include the DUT with `ahdl_include "<module>.va"`.
- Use a single `tran` analysis and include the required `save` signals for checker evaluation.


## Public Evaluation Contract (Non-Gold)

This section states evaluator-facing constraints that must be visible to the generated artifact.
It does not prescribe the internal implementation or reveal a gold solution.

Final EVAS transient setting:

```spectre
tran tran stop=80n maxstep=20p errpreset=conservative
```

Required public waveform columns in `tran.csv`:

- `time`, `out`

Use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Timing/checking-window contract:

- Public stimulus nodes used by the reference harness include: `VDD`, `VSS`, `ref`.
