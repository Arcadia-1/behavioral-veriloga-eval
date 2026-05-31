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
