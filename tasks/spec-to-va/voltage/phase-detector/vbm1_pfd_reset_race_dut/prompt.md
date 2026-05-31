# Task: vbm1_pfd_reset_race_dut

Write a pure voltage-domain Verilog-A module for a PFD reset-race UP/DN generator.

The DUT module is `pfd_updn` with ports `VDD, VSS, REF, DIV, UP, DN`. All ports are electrical; digital-control ports use 0/0.9 V logic levels.

Required behavior:
- Set `UP` high on a rising `REF` edge and set `DN` high on a rising `DIV` edge.
- If the opposite output is already high when an edge arrives, clear both outputs to model the reset-race behavior.
- Drive `UP` and `DN` as smoothed voltage-domain logic levels.

Use voltage contributions only. Do not use current contributions, `ddt()`, or `idt()`.

Return exactly one complete Verilog-A file named `pfd_updn.va`.
