# Burst Clock Source Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `clk_burst_gen.va`: `clk_burst_gen`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_ACTIVE_LOW_RESET`: While RST_N is below vth, CLK_OUT is low and the burst frame counter is restarted.
- `P_FRAME_START`: After reset release, rising CLK crossings advance a repeating frame of div input-clock cycles beginning at position 0.
- `P_TWO_CYCLE_BURST`: At frame positions 0 and 1, CLK_OUT passes the voltage-coded CLK waveform, including its high and low phases.
- `P_QUIET_REMAINDER`: At frame positions 2 through div minus 1, CLK_OUT remains low regardless of CLK level.
- `P_FRAME_REPEAT`: The two-cycle burst followed by the quiet remainder repeats every div rising CLK crossings.
- `P_OUTPUT_LEVELS`: CLK_OUT uses 0 V and vdd as its voltage-coded low and high levels.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `clk_burst_gen.va`.
Every supplied `.va` file is editable; do not add or omit files.
