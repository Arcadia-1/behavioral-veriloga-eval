# ADC Static Linearity Monitor Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `ADC Static Linearity Monitor` DUT. The evaluator runs the same submitted bytes
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

- `P_STROBE_UPDATE`: The retained error metric updates only on rising crossings of vsample through vth and holds between strobes.
- `P_IDEAL_CODE`: At a strobe, vin is clipped to 0 through vref and mapped to the ideal three-bit bin-floor code.
- `P_OBSERVED_CODE`: At a strobe, d2 through d0 are threshold-decoded as an unsigned three-bit word with d2 as MSB and d0 as LSB.
- `P_ABSOLUTE_ERROR`: Each sampled error is the absolute difference in codes between the ideal and observed three-bit words.
- `P_MAX_RETENTION`: maxerr never decreases during a run and represents the largest sampled absolute code error seen so far.
- `P_METRIC_SCALE`: maxerr equals the retained maximum code error multiplied by lsb_out, with smoothing set by tr.

The required trace names are: `time`, `vsample`, `vin`, `d2`, `d1`, `d0`, `maxerr`.

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
