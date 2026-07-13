# Multiphase Clock Generator 4ph

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `multiphase_clock_generator_4ph.va`: `multiphase_clock_generator_4ph`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_PERIOD`: Each output repeats with a 20 ns period.
- `P_DUTY_CYCLE`: Each output has approximately 50 percent duty cycle.
- `P_PHASE_OFFSETS`: Relative to clk0, corresponding rising edges of clk90, clk180, and clk270 lag by 5 ns, 10 ns, and 15 ns respectively.
- `P_PHASE_STABILITY`: The output phase ordering and offsets remain stable across repeated periods.
- `P_OUTPUT_LEVELS`: All clocks use 0 V and vdd levels with finite transition smoothing set by tr.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `multiphase_clock_generator_4ph.va`.
Do not add or omit artifacts.
