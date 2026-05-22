# Task: vbr1_l1_pfd_up_dn_logic:tb

## Release Task Contract

- Form: `tb`
- Level: `L1`
- Category: PLL / Clock / Event Timing
- Base function: PFD UP/DN logic
- Domain: `voltage`
- Target artifact(s): `tb_pfd_reset_race_ref.scs`
- Supplied/reference support artifact(s): `pfd_updn.va`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Generate only the Spectre transient testbench artifact(s); do not generate hidden checker logic.
- Instantiate the supplied/public DUT module(s), drive a public transient scenario, and save the required observables.

## Public DUT Interface To Instantiate

- `pfd_updn.va` declares module `pfd_updn` with positional ports: `VDD`, `VSS`, `REF`, `DIV`, `UP`, `DN`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=300n maxstep=10p errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `ref`
- `div`
- `up`
- `dn`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

Public stimulus/source nodes visible in the reference harness include:

- `vdd`
- `vss`
- `ref`
- `div`

## Public Behavior Checks

- `up_and_dn_pulses_exist`
- `overlap_window_is_bounded`
- `outputs_clear_after_race`

## Output Contract

Return exactly one source artifact named `tb_pfd_reset_race_ref.scs`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_pfd_reset_race_tb

Write a Spectre testbench for a PFD reset-race UP/DN generator DUT.

The DUT module is `pfd_updn` with ports `VDD, VSS, REF, DIV, UP, DN`. All ports are electrical; digital-control ports use 0/0.9 V logic levels. The candidate DUT file will be available as `pfd_updn.va`; include it with `ahdl_include` and instantiate the DUT using the exact module and port names.

The testbench must exercise:
- Set `UP` high on a rising `REF` edge and set `DN` high on a rising `DIV` edge.
- If the opposite output is already high when an edge arrives, clear both outputs to model the reset-race behavior.
- Drive `UP` and `DN` as smoothed voltage-domain logic levels.

Stimulus and observability requirements:
- Use close REF/DIV edge timing and a small maxstep so reset-race ordering is observable.
- Save `REF`, `DIV`, `UP`, and `DN`.

Return exactly one Spectre testbench file named `tb_pfd_reset_race_ref.scs`.
