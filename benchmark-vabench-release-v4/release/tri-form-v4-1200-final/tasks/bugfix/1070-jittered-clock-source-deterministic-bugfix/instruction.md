# Deterministic Jittered Clock Source Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `deterministic_jittered_clock.va`: `deterministic_jittered_clock`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_NOMINAL_CLOCK`: With jitter_en below vth, clk_out has a constant 10 ns half-period and 20 ns full period.
- `P_SEED_DECODE`: Seed7:seed0 is sampled through vth only at each output transition and interpreted as one unsigned eight-bit seed with seed7 as MSB; seed changes affect the next scheduled half-period, not the already scheduled current edge.
- `P_EDGE_MODULATION`: For edge index k, the next half-period is 10 ns plus (((seed + 3*k) modulo 5) minus 2) times 0.8 ns.
- `P_REPEATABILITY`: With constant seed and enable history, the modulo-5 half-period sequence repeats every five output transitions; identical input histories also produce the same edge-time sequence on repeated runs.
- `P_TIMING_BOUNDS`: Every jitter-enabled half-period remains within the public modulation range from 8.4 ns through 11.6 ns.
- `P_OUTPUT_LEVELS`: clk_out uses 0 V and vdd levels with finite transition smoothing set by tr.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `deterministic_jittered_clock.va`.
Every supplied `.va` file is editable; do not add or omit files.
