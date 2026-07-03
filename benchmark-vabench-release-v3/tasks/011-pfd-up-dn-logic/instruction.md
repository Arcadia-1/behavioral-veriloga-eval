# PFD UP/DN Reset-Race Logic

Implement `pfd_updn.va` in Verilog-A.

## Interface

```verilog
module pfd_updn (
    inout  electrical VDD,
    inout  electrical VSS,
    input  electrical REF,
    input  electrical DIV,
    output electrical UP,
    output electrical DN
);
```

## Required Behavior

This task asks for the `pfd_updn` behavioral DUT module, not a Spectre
testbench. The module is a voltage-domain phase-frequency detector UP/DN
generator with reset-race clearing.

Support these public parameters and legal overrides:

| Parameter | Default | Unit / range | Contract |
| --- | ---: | --- | --- |
| `vth` | `0.45` | V | Rising-edge threshold for `REF` and `DIV`. |
| `tedge` | `20 ps` | time, `(0:inf)` | Rise/fall smoothing for `UP` and `DN`. |

Required observable behavior:

- Detect rising `REF` and `DIV` crossings at `vth`.
- Set `UP` high on a rising `REF` edge and keep it high until a qualifying
  reset-race clear.
- Set `DN` high on a rising `DIV` edge and keep it high until a qualifying
  reset-race clear.
- If a rising edge arrives while the opposite output state is already high,
  clear both `UP` and `DN` immediately. This must work when `REF` leads `DIV`
  and when `DIV` leads `REF`.
- Falling input edges must not set either output.
- After a reset-race clear, both outputs must remain low until the next rising
  input edge.
- Do not intentionally hold both `UP` and `DN` high beyond analog smoothing
  overlap.
- Drive `UP` and `DN` as smoothed voltage-domain logic levels referenced to
  `VDD` for high and `VSS` for low.

Use voltage contributions only. Do not use current contributions, `ddt()`,
`idt()`, transistor-level devices, AC/noise analysis, checker logic, private
test hooks, or simulator-private side channels.

## Output

Return exactly one source artifact named `pfd_updn.va`.
