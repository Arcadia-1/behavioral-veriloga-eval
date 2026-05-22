# Task: vbm1_pfd_reset_race_e2e

Write both the Verilog-A DUT and Spectre testbench for a PFD reset-race UP/DN generator.

The DUT module is `pfd_updn` with ports `VDD, VSS, REF, DIV, UP, DN`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required DUT behavior:
- Set `UP` high on a rising `REF` edge and set `DN` high on a rising `DIV` edge.
- If the opposite output is already high when an edge arrives, clear both outputs to model the reset-race behavior.
- Drive `UP` and `DN` as smoothed voltage-domain logic levels.

Required testbench behavior:
- Use close REF/DIV edge timing and a small maxstep so reset-race ordering is observable.
- Save `REF`, `DIV`, `UP`, and `DN`.

Use voltage contributions only in the Verilog-A DUT. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly two files: `pfd_updn.va` and `tb_pfd_reset_race_ref.scs`.
