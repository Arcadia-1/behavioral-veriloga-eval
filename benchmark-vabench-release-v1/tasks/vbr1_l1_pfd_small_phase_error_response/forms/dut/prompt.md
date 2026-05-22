# Task: vbr1_l1_pfd_small_phase_error_response:dut

## Release Task Contract

- Form: `dut`
- Level: `L1`
- Category: PLL / Clock / Event Timing
- Base function: PFD small phase-error response
- Domain: `voltage`
- Target artifact(s): `pfd_updn.va`
- Supplied/reference support artifact(s): `tb_pfd_small_phase_ref.scs`
- Visible context: public task, interface, artifact, stimulus, and observable contract only.
- Hidden evaluator boundary: deterministic checker and EVAS/Spectre validation are external; do not generate checker logic.

## Form-Specific Requirements

- Implement only the requested Verilog-A DUT artifact(s); do not generate a Spectre testbench in this form.
- Preserve the public module names, port order, parameters, and waveform observable names.

## Public Verilog-A Interface

- `pfd_updn.va` declares module `pfd_updn` with positional ports: `VDD`, `VSS`, `REF`, `DIV`, `UP`, `DN`.

## Public Testbench And Observable Contract

Public transient setting used by the release harness:

```spectre
tran tran stop=300n maxstep=5p errpreset=conservative
```

The release harness expects these exact public scalar observables:

- `ref`
- `div`
- `up`
- `dn`

When this form generates a testbench, use plain scalar save names for these observables; do not rely on instance-qualified or aliased save names.

## Public Behavior Checks

- `short_up_pulses_present_for_small_phase_error`
- `up_dn_overlap_not_sustained`
- `dn_not_sustained_for_ref_leading_div_stimulus`

## Output Contract

Return exactly one source artifact named `pfd_updn.va`.
Do not include explanatory prose outside the source artifact contents.

## Task-Specific Public Description

# Task: vbm1_pfd_small_phase_error_response_dut

Write a pure voltage-domain Verilog-A DUT for a phase-frequency detector that
responds correctly to small REF/DIV phase errors.

Return exactly one complete Verilog-A file named `pfd_updn.va`.

## Module Contract

Implement this module declaration and port order:

```verilog
module pfd_updn(VDD, VSS, REF, DIV, UP, DN);
```

All ports are `electrical`. `VDD` and `VSS` are supply rails, `REF` and `DIV`
are input clocks, and `UP` and `DN` are output pulses. Public stimulus uses
`VDD=0.9 V`, `VSS=0 V`, and small REF/DIV phase offsets.

## Required Behavior

- A rising edge on `REF` asserts `UP`.
- A rising edge on `DIV` asserts `DN`.
- When both internal UP and DN states have arrived, reset both outputs back to
  low so overlap is short and bounded.
- For a small REF-leading-DIV phase error, generate repeated short `UP` pulses
  and no sustained `DN` pulse train.
- Drive output HIGH from `VDD` and LOW from `VSS`, read dynamically.
- Stay in the pure voltage-domain behavioral subset. Do not use current
  contributions, `ddt`, or `idt`.

## Public Evaluation Observables

The public checker saves `REF`, `DIV`, `UP`, and `DN`. It checks that small
phase-error stimulus produces bounded `UP` pulse activity, that `DN` remains
low except for reset overlap transients, and that UP/DN overlap is not
sustained.
