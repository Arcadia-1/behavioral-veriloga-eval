# Task: vbr1_l1_debounce_latch:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Digital and Event-Driven Logic
- Base function: Debounce latch
- Domain: `voltage`
- Target artifact(s): `debounce_latch.va`, `tb_debounce_latch_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `debounce_latch.va`, `tb_debounce_latch_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `debounce_latch.va` declares module `debounce_latch` with positional ports: `sig`, `rst_n`, `out`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=140n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `sig`
- `rst_n`
- `out`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `sig`
- `rst_n`

## Public Behavior Checks

- `short_glitch_rejected`
- `stable_high_qualified_after_delay`
- `falling_sig_clears_output`

## Output Contract

Return exactly these source artifacts:

- `debounce_latch.va`
- `tb_debounce_latch_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_debounce_latch_e2e

Write both the Verilog-A DUT and Spectre testbench for a debounced latch with delayed qualification.

The DUT module is `debounce_latch` with ports `sig, rst_n, out`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Use active-low reset `rst_n`; reset forces `out` low and cancels any pending qualification.
- On a rising `sig` edge while reset is released, arm a 12 ns qualification timer.
- On the timer event, set `out` high only if `sig` and `rst_n` are still high; falling `sig` clears or cancels the output.

Required testbench behavior:
- Create short rejected pulses and longer accepted pulses on `sig` after reset releases.
- Run long enough to observe at least one rejected pulse and one qualified high output.
- Save `sig`, `rst_n`, and `out`.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `debounce_latch.va` and `tb_debounce_latch_ref.scs`.
