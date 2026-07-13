# Programmable Stimulus Sequencer Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Programmable Stimulus Sequencer` DUT. The evaluator runs the same submitted bytes
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

- `P_RESET_IDLE`: When rst is above the 0.45 V control threshold, out is held near 0.45 V and metric is low.
- `P_RAMP_MODE`: For mode below 0.30 V outside reset, out produces a monotonic ramp segment from about 0.18 V toward 0.45 V and metric is near 0.20 V.
- `P_CHIRP_MODE`: For mode from 0.30 V through below 0.60 V, out is a sine segment centered near 0.45 V whose instantaneous frequency increases over the segment, with metric near 0.50 V.
- `P_BURST_GATE`: For mode at or above 0.60 V and gate high, out produces a deterministic PRBS-like burst between the low and high stimulus levels.
- `P_BURST_IDLE`: In burst mode with gate low, out returns near 0.45 V and metric reports the idle rather than active-burst status.
- `P_CONTROL_DRIVEN_SELECTION`: Mode and gate behavior follows the voltage-coded inputs over arbitrary legal control schedules rather than a fixed stimulus timeline.

The required trace names are: `time`, `clk`, `rst`, `mode`, `gate`, `out`, `metric`.

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
