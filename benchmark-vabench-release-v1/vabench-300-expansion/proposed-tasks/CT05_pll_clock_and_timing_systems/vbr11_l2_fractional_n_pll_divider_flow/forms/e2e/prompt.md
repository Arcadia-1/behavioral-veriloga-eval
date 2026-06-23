# Task: fractional_n_pll_divider:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L2`
- Category: PLL Clock and Timing Systems
- Base function: Fractional-N divider and accumulator flow
- Domain: `voltage`
- Target artifact(s): `fractional_n_pll_divider.va`, `tb_fractional_n_pll_divider.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## L2 Background And Claim Boundary

This Level-2 row is a behavioral composition/flow task for Fractional-N divider and accumulator flow. It should expose intermediate state, multi-stage behavior, or a closed-loop relation through the public observables below.
Stay within the listed voltage-domain/event-driven contract. Do not use transistor-level devices, current-domain loads, AC/noise analysis, S-parameters, or hidden checker logic unless the public contract explicitly lists them.
Paper-facing claims for this row are limited to the public behavior checks below; do not broaden the task into full silicon implementation, layout, device physics, or unlisted performance metrics.

## Form-Specific Requirements

- Generate all target artifacts: `fractional_n_pll_divider.va`, `tb_fractional_n_pll_divider.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.
- The generated Verilog-A file(s) `fractional_n_pll_divider.va` must be co-located with the generated Spectre testbench.
- Include the generated DUT exactly with `ahdl_include "fractional_n_pll_divider.va"` in the generated testbench.
- Use Spectre AHDL instance syntax with the instance name first and module name last: `XNAME (node1 node2 ...) module_name`.
- Never write module-first syntax such as `module_name instance_name (...)`; that is not the release Spectre testbench syntax.

## Public Verilog-A Interface

- `fractional_n_pll_divider.va` declares module `fractional_n_pll_divider` with positional ports: `in`, `clk`, `rst`, `out`, `metric`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=260n maxstep=500p
```

Public stimulus/source nodes visible in the reference harness include:

- `clk`
- `rst`
- `in`

## Public Spectre Testbench Scaffold

When this form generates a `.scs` testbench, use the following public skeleton shape. Fill in only the public stimulus details required by the task; do not copy or emit hidden checker logic.

```spectre
simulator lang=spectre
global 0
ahdl_include "fractional_n_pll_divider.va"

Xdut (in clk rst out metric) fractional_n_pll_divider

tran tran stop=260n maxstep=500p
```

Critical syntax rules:

- Every Verilog-A DUT/support file used by the testbench must have a literal `ahdl_include "<file>.va"` line in the `.scs` artifact.
- Spectre AHDL instances use instance-first/module-last syntax: `XNAME (node1 node2 ...) module_name`.
- Do not use module-first syntax such as `module_name instance_name (...)`.
- Keep saved names as plain scalar public observables, not instance-qualified aliases.

## Public Behavior Checks

- `fractional_n_pll_divider_full_behavior`
- `period_statistics_near_miss_rejection`

## Output Contract

Return exactly these source artifacts:

- `fractional_n_pll_divider.va`
- `tb_fractional_n_pll_divider.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: fractional_n_pll_divider:e2e

## vaBench-300 v1.1 Task-Specific Contract

- Status: `provisional_v1.1_management`
- Paper score: `disabled_until_fresh_spectre_certification`
- Form: `e2e`
- Family: `end-to-end`
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

Create a divider, stimulus, and period-statistics flow.

Do not satisfy this task with a generic state scaffold. The implementation
must preserve the named circuit-function behavior and expose both the
`out` waveform and the task-specific `metric` monitor.
