# Deterministic Jittered Clock Source

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `deterministic_jittered_clock.va`: `deterministic_jittered_clock`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_NOMINAL_CLOCK`: With jitter_en below vth, clk_out has a constant 10 ns half-period and 20 ns full period.
- `P_SEED_DECODE`: Seed7:seed0 is sampled through vth only at each output transition and interpreted as one unsigned eight-bit seed with seed7 as MSB; seed changes affect the next scheduled half-period, not the already scheduled current edge.
- `P_EDGE_MODULATION`: For edge index k, the next half-period is 10 ns plus (((seed + 3*k) modulo 5) minus 2) times 0.8 ns.
- `P_REPEATABILITY`: With constant seed and enable history, the modulo-5 half-period sequence repeats every five output transitions; identical input histories also produce the same edge-time sequence on repeated runs.
- `P_TIMING_BOUNDS`: Every jitter-enabled half-period remains within the public modulation range from 8.4 ns through 11.6 ns.
- `P_OUTPUT_LEVELS`: clk_out uses 0 V and vdd levels with finite transition smoothing set by tr.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `deterministic_jittered_clock.va`.
Do not add or omit artifacts.
