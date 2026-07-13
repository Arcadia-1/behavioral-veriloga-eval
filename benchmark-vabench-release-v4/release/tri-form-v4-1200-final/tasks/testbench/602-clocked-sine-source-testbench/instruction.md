# Clocked Sine Source Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Clocked Sine Source` DUT. The evaluator runs the same submitted bytes
against the correct DUT and five anonymous semantic negative DUTs. Your
testbench must accept the correct DUT and expose all five behavioral faults.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

The exact read-only source paths, modules, ports, instance names, and ordered
terminal bindings are declared in `solver_contract.json`.

## Public Parameter Contract

Honor the public parameter declarations in `solver_contract.json` when choosing
stimulus and coverage.

## Required Behavior

Create stimulus and save traces sufficient for the fixed evaluator oracle to check:

- `P_RESET_COMMON_MODE`: While RST_N is below vth, both outputs hold near vdd divided by two.
- `P_RISING_EDGE_SAMPLE`: After reset release, VOUT_P updates only on rising CLK crossings through vth.
- `P_SAMPLED_SINE`: At each qualifying clock edge, VOUT_P samples vdd/2 plus ampl times sin(2*pi*freq*time), plus the optional seeded perturbation.
- `P_REFERENCE_SIDE_COMMON_MODE`: VOUT_N remains at vdd divided by two during reset and active sampling.
- `P_INTEREDGE_HOLD`: Both outputs hold their sampled values between CLK events rather than continuously recomputing the sine or perturbation.
- `P_SEEDED_REPEATABILITY`: For fixed SEED, sigma, controls, and timing, the sampled perturbation sequence and outputs are repeatable; sigma zero removes the perturbation.

The required trace names are: `time`, `clk`, `rst_n`, `vinp`, `vinn`, `vamp_p`, `vamp_n`.

## Modeling Constraints

- Submit one self-contained top-level transient `.scs` file.
- Use only the exact declared testbench include paths and public DUT interfaces.
- Do not redefine the DUT, drive declared DUT outputs, inspect private internals,
  access undeclared files, or emit a self-reported result.
- Respect every public resource limit in `solver_contract.json`.
- Missing traces, setup errors, and invalid runs do not count as behavioral kills.

## Output Contract

Return exactly one submission-root-relative artifact named `testbench.scs`. Do not return a DUT,
checker, script, data file, waveform, or auxiliary deck.
