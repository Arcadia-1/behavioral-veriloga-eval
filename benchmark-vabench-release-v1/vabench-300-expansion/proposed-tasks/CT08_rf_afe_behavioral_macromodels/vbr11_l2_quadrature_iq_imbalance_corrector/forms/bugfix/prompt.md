# Task: quadrature_iq_imbalance_corrector:bugfix

## Release Task Contract

- Form: `bugfix`
- Level: `L2`
- Category: RF and AFE Behavioral Macromodels
- Base function: Quadrature gain/phase imbalance corrector
- Domain: `voltage`
- Target artifact(s): `quadrature_iq_imbalance_corrector.va`
- Supplied/reference support artifact(s): `tb_quadrature_iq_imbalance_corrector.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## L2 Background And Claim Boundary

This Level-2 row is a behavioral composition/flow task for Quadrature gain/phase imbalance corrector. It should expose intermediate state, multi-stage behavior, or a closed-loop relation through the public observables below.
Stay within the listed voltage-domain/event-driven contract. Do not use transistor-level devices, current-domain loads, AC/noise analysis, S-parameters, or hidden checker logic unless the public contract explicitly lists them.
Paper-facing claims for this row are limited to the public behavior checks below; do not broaden the task into full silicon implementation, layout, device physics, or unlisted performance metrics.

## Form-Specific Requirements

- Repair the supplied buggy Verilog-A artifact while preserving the public module interface and artifact boundary.
- Use the buggy source plus the public intended behavior below; do not change the companion testbench contract.

## Public Interface To Preserve

- `quadrature_iq_imbalance_corrector.va` declares module `quadrature_iq_imbalance_corrector` with positional ports: `in`, `clk`, `rst`, `out`, `metric`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=260n maxstep=500p
```


## Public Behavior Checks

- `quadrature_iq_imbalance_corrector_full_behavior`
- `coefficient_direction_bug_near_miss_rejection`

## Observed Mismatch Framing

The supplied buggy artifact violates one or more public behavior checks above under the release validation testbench.
Repair the observable behavior without renaming modules, changing ports, or weakening the public testbench contract.

## Output Contract

Return exactly one source artifact named `quadrature_iq_imbalance_corrector.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: quadrature_iq_imbalance_corrector:bugfix

## vaBench-300 v1.1 Task-Specific Contract

- Status: `provisional_v1.1_management`
- Paper score: `disabled_until_fresh_spectre_certification`
- Form: `bugfix`
- Family: `bugfix`
- Level: `L2`
- Track: `core`
- Difficulty: `D3`
- Category: RF and AFE Behavioral Macromodels
- Base function target: Quadrature gain/phase imbalance corrector
- Domain: voltage-domain behavioral Verilog-A

This row has been rebuilt from the original v1.1 management scaffold into
a task-specific benchmark candidate. It remains outside the paper score
denominator until fresh EVAS/Spectre certification is recorded for this
rebuilt source asset.

## Current Public Interface

- Verilog-A artifact: `quadrature_iq_imbalance_corrector.va`
- Spectre testbench artifact: `tb_quadrature_iq_imbalance_corrector.scs`
- Module name: `quadrature_iq_imbalance_corrector`
- Positional ports: `in`, `clk`, `rst`, `out`, `metric`
- Port roles:
  - `in`: voltage-coded stimulus input.
  - `clk`: voltage-coded event clock, low=0 V and high=1 V.
  - `rst`: voltage-coded reset pulse.
  - `out`: bounded state/output monitor.
  - `metric`: derived state metric monitor.

## Task-Specific Observable Contract

- Behavior: quadrature gain/phase imbalance correction macro with positive input correlation and error metric.
- Observable: out is the corrected channel monitor; metric is the post-correction quality estimate.
- Checker: output remains positively correlated with input and final correction metric is high.
- Rising `rst` clears state before the measurement window.
- Rising `clk` events drive the discrete-time behavior.
- The Spectre scaffold instantiates the DUT with instance-first AHDL syntax
  and records `time`, `in`, `clk`, `rst`, `out`, and `metric`.

## Task Goal

Repair I/Q sign, phase unit, or coefficient update direction.

Do not satisfy this task with a generic state scaffold. The implementation
must preserve the named circuit-function behavior and expose both the
`out` waveform and the task-specific `metric` monitor.
