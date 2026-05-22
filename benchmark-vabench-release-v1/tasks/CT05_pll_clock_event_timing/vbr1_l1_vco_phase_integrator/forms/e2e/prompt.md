# Task: vbr1_l1_vco_phase_integrator:e2e

## Release Task Contract

- Form: `e2e`
- Level: `L1`
- Category: PLL / Clock / Event Timing
- Base function: VCO phase integrator
- Domain: `voltage`
- Target artifact(s): `tb_vco_phase_integrator_ref.scs`, `vco_phase_integrator.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate all target artifacts: `tb_vco_phase_integrator_ref.scs`, `vco_phase_integrator.va`.
- The Spectre testbench must exercise the generated DUT/system through public observables; do not generate hidden checker logic.

## Public Verilog-A Interface

- `vco_phase_integrator.va` declares module `vco_phase_integrator` with positional ports: `vctrl`, `phase`, `clk`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=180n maxstep=500p
```

The release harness expects these exact public scalar observables:

- `vctrl`
- `phase`
- `clk`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vctrl`

## Public Behavior Checks

- `phase_span_covers_nearly_full_wrap`
- `clock_toggles_on_phase_wrap`
- `late_edge_rate_exceeds_early_edge_rate`

## Output Contract

Return exactly these source artifacts:

- `tb_vco_phase_integrator_ref.scs`
- `vco_phase_integrator.va`

Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_vco_phase_integrator_e2e

Write both the Verilog-A DUT and Spectre testbench for a timer-driven VCO phase integrator.

The DUT module is `vco_phase_integrator` with ports `vctrl, phase, clk`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Use a 1 ns timer update and increment phase by `0.03 + 0.09 * V(vctrl)` at each update.
- Wrap phase at 1.0 and toggle `clk` on each wrap.
- Drive both `phase` and `clk` through `transition()`.

Required testbench behavior:
- Drive `vctrl` through low and higher-control intervals so the late clock edge rate is faster than the early edge rate.
- Save `vctrl`, `phase`, and `clk` across a long transient.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `vco_phase_integrator.va` and `tb_vco_phase_integrator_ref.scs`.
