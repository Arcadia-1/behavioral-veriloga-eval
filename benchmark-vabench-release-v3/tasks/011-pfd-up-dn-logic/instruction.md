# PFD Up DN Logic

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: PLL Clock and Timing Systems
- Base function: PFD UP/DN logic
- Domain: `voltage`
- Target artifact(s): `pfd_updn.va`
- Supplied/reference support artifact(s): `tb_pfd_reset_race_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `pfd_updn.va` declares module `pfd_updn` with positional ports: `VDD`, `VSS`, `REF`, `DIV`, `UP`, `DN`.

## Public Testbench And Observable Contract

Public transient setting used by the evaluator:

```spectre
tran tran stop=300n maxstep=5n errpreset=conservative
```

The evaluator expects these exact public scalar observables:

- `ref`
- `div`
- `up`
- `dn`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `up_and_dn_pulses_exist`
- `overlap_window_is_bounded`
- `outputs_clear_after_race`

## Output Contract

Return exactly one source artifact named `pfd_updn.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Description

## PFD UP/DN Reset-Race DUT

Write a pure voltage-domain Verilog-A module for a PFD reset-race UP/DN generator.

The DUT module is `pfd_updn` with ports `VDD, VSS, REF, DIV, UP, DN`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Detect rising `REF` and `DIV` crossings at the logic threshold. The default threshold is 0.45 V.
- Set `UP` high on a rising `REF` edge and keep it high until the next qualifying reset-race event.
- Set `DN` high on a rising `DIV` edge and keep it high until the next qualifying reset-race event.
- If a rising edge arrives while the opposite output state is already high, clear both `UP` and `DN` immediately. This must work both when `REF` leads `DIV` and when `DIV` leads `REF`.
- Falling input edges must not set either output.
- After the reset-race clear, both outputs must return low and remain low until the next rising input edge.
- Do not intentionally hold both `UP` and `DN` high beyond the analog transition overlap caused by smoothing.
- Drive `UP` and `DN` as smoothed voltage-domain logic levels referenced to `VDD` for high and `VSS` for low. The default transition time is 20 ps.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `pfd_updn.va`.
