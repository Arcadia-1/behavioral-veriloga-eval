# Task: vbr1_l1_window_comparator_detector:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: Comparator and Decision Circuits
- Base function: Window comparator/detector
- Domain: `voltage`
- Target artifact(s): `window_comparator_ref.va`, `tb_window_comparator_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `window_comparator_ref.va`, `tb_window_comparator_ref.scs`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `window_comparator_ref.va` declares module `window_comparator_ref` with positional ports: `VDD`, `VSS`, `vin`, `out`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=90n maxstep=20p errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `vin`
- `out`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `VDD`
- `VSS`
- `vin`

## Public Behavior Checks

- `true_window_comparator`

## Output Contract

Return exactly these source artifacts:

- `window_comparator_ref.va`
- `tb_window_comparator_ref.scs`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

Implement a true voltage-domain window comparator and one Spectre transient
testbench.

DUT requirements:

- use module `window_comparator_ref` with the public port order listed above
- expose `vlow=0.3` and `vhigh=0.6` as real threshold parameters
- drive `out` high only while `vlow < V(vin,VSS) < vhigh`
- drive `out` low when `V(vin,VSS) <= vlow` or `V(vin,VSS) >= vhigh`
- handle both rising and falling ramps through both thresholds
- use voltage-domain `transition()` output drive only

Testbench requirements:

- include `window_comparator_ref.va` via `ahdl_include`
- use `VDD = 0.9 V` and `VSS = 0 V`
- drive `vin` with a triangular PWL waveform that sweeps below `0.3 V`,
  through the window, above `0.6 V`, and back down through the window
- run `tran tran stop=90n maxstep=20p errpreset=conservative`
- save exactly `vin` and `out`
- avoid current-domain contributions, dynamic analog operators, transistor
  devices, AC analysis, and noise analysis
