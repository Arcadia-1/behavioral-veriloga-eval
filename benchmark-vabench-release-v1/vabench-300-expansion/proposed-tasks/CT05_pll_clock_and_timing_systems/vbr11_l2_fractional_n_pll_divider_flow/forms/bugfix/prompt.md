# Task: fractional_n_pll_divider:bugfix

## Release Task Contract

- Form: `bugfix`
- Level: `L2`
- Category: PLL Clock and Timing Systems
- Base function: Fractional-N divider and accumulator flow
- Domain: `voltage`
- Target artifact(s): `fractional_n_pll_divider.va`
- Supplied/reference support artifact(s): `tb_fractional_n_pll_divider.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## L2 Background And Claim Boundary

This Level-2 row is a behavioral composition/flow task for Fractional-N divider and accumulator flow. It should expose intermediate state, multi-stage behavior, or a closed-loop relation through the public observables below.
Stay within the listed voltage-domain/event-driven contract. Do not use transistor-level devices, current-domain loads, AC/noise analysis, S-parameters, or hidden checker logic unless the public contract explicitly lists them.
Paper-facing claims for this row are limited to the public behavior checks below; do not broaden the task into full silicon implementation, layout, device physics, or unlisted performance metrics.

## Form-Specific Requirements

- Repair the supplied buggy Verilog-A artifact while preserving the public module interface and artifact boundary.
- Use the buggy source plus the public intended behavior below; do not change the companion testbench contract.

## Public Interface To Preserve

- `fractional_n_pll_divider.va` declares module `fractional_n_pll_divider` with positional ports: `in`, `clk`, `rst`, `out`, `metric`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=260n maxstep=500p
```


## Public Behavior Checks

- `fractional_n_pll_divider_full_behavior`
- `wrap_pulse_width_bug_near_miss_rejection`

## Observed Mismatch Framing

The supplied buggy artifact violates one or more public behavior checks above under the release validation testbench.
Repair the observable behavior without renaming modules, changing ports, or weakening the public testbench contract.

## Output Contract

Return exactly one source artifact named `fractional_n_pll_divider.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: fractional_n_pll_divider:bugfix

## vaBench-300 v1.1 Task-Specific Contract

- Status: `provisional_v1.1_management`
- Paper score: `disabled_until_fresh_spectre_certification`
- Form: `bugfix`
- Family: `bugfix`
- Level: `L2`
- Track: `core`
- Difficulty: `D3`
- Category: PLL Clock and Timing Systems
- Base function target: Fractional-N divider and accumulator flow
- Domain: voltage-domain behavioral Verilog-A

This row has been rebuilt from the original v1.1 management scaffold into
a task-specific benchmark candidate. It remains outside the paper score
denominator until fresh EVAS/Spectre certification is recorded for this
rebuilt source asset.

## Current Public Interface

- Verilog-A artifact: `fractional_n_pll_divider.va`
- Spectre testbench artifact: `tb_fractional_n_pll_divider.scs`
- Module name: `fractional_n_pll_divider`
- Positional ports: `in`, `clk`, `rst`, `out`, `metric`
- Port roles:
  - `in`: voltage-coded stimulus input.
  - `clk`: voltage-coded event clock, low=0 V and high=1 V.
  - `rst`: voltage-coded reset pulse.
  - `out`: bounded state/output monitor.
  - `metric`: derived state metric monitor.

## Task-Specific Observable Contract

- Behavior: fractional-N divider accumulator that emits carry pulses at the requested average divide ratio.
- Observable: out is the carry/pulse stream; metric is the normalized accumulator residue.
- Checker: pulse density and residue swing match a fractional accumulator rather than an integer divider.
- Rising `rst` clears state before the measurement window.
- Rising `clk` events drive the discrete-time behavior.
- The Spectre scaffold instantiates the DUT with instance-first AHDL syntax
  and records `time`, `in`, `clk`, `rst`, `out`, and `metric`.

## Task Goal

Repair a modulo wrap, pulse-width, or initial-phase bug.

Do not satisfy this task with a generic state scaffold. The implementation
must preserve the named circuit-function behavior and expose both the
`out` waveform and the task-specific `metric` monitor.
