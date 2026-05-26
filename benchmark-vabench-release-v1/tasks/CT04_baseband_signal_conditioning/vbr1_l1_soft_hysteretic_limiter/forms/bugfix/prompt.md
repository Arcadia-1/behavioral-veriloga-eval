# Task: vbr1_l1_soft_hysteretic_limiter:bugfix

## Release Task Contract

- Form: `bugfix`
- Level: `L1`
- Category: Baseband Signal Conditioning
- Base function: Soft/hysteretic limiter
- Domain: `voltage`
- Target artifact(s): `dut_fixed.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate the repaired target artifact: `dut_fixed.va`.
- Preserve the public module name, positional ports, voltage-domain behavior, and observable contract.

## Public Verilog-A Interface

- `soft_hysteretic_limiter.va` declares module `soft_hysteretic_limiter` with positional ports from the public port contract below.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=80n maxstep=0.5n
```

The release harness expects these exact public scalar observables:

```text
clk rst vin out metric
```

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- smooth_limiting
- hysteresis_state_memory
- bounded_output

## Output Contract

Return exactly these source artifacts:

- `dut_fixed.va`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

### Soft/hysteretic limiter (bugfix)

Repair the supplied buggy Verilog-A implementation. Known defect: The buggy implementation collapses the hysteresis thresholds into a single threshold.

Behavioral intent:

Limit a voltage signal with smooth compression and stateful hysteresis around thresholds.

Module name: `soft_hysteretic_limiter`.
Domain: pure voltage-domain behavioral Verilog-A.
Do not use current contributions, transistor-level devices, AC/noise analysis,
or KCL/KVL solving assumptions.


Public port contract:

```verilog
module soft_hysteretic_limiter(clk, rst, vin, out, metric);
input clk, rst, vin;
output out, metric;
electrical clk, rst, vin, out, metric;
```

Signal contract:

clk and rst are voltage-coded logic signals, low=0 V and high=0.9 V with threshold 0.45 V. vin is an analog voltage stimulus. out is the bounded conditioned voltage. metric exposes the filter/settling internal response.

Saved waveform columns:

```text
clk rst vin out metric
```

Public behavior checks:

- smooth_limiting
- hysteresis_state_memory
- bounded_output

Public transient contract:

```spectre
tran tran stop=80n maxstep=0.5n
```
