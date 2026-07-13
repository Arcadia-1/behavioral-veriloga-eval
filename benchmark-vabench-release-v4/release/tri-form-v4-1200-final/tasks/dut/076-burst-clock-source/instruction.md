# Burst Clock Source

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `clk_burst_gen.va`: `clk_burst_gen`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_ACTIVE_LOW_RESET`: While RST_N is below vth, CLK_OUT is low and the burst frame counter is restarted.
- `P_FRAME_START`: After reset release, rising CLK crossings advance a repeating frame of div input-clock cycles beginning at position 0.
- `P_TWO_CYCLE_BURST`: At frame positions 0 and 1, CLK_OUT passes the voltage-coded CLK waveform, including its high and low phases.
- `P_QUIET_REMAINDER`: At frame positions 2 through div minus 1, CLK_OUT remains low regardless of CLK level.
- `P_FRAME_REPEAT`: The two-cycle burst followed by the quiet remainder repeats every div rising CLK crossings.
- `P_OUTPUT_LEVELS`: CLK_OUT uses 0 V and vdd as its voltage-coded low and high levels.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `clk_burst_gen.va`.
Do not add or omit artifacts.
