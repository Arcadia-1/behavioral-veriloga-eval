# ADC Zoom Timing Sequencer

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `adc_zoom_timing_sequencer.va`: `adc_zoom_timing_sequencer`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_GENERATE_A_REPEATING_32_NS_COMPACT`: Generate a repeating 32 ns compact ADC timing frame with these high windows: `rst` from 0.5 to 0.8 ns; `s` from 1.5 to 2.5 ns; `sar` from 3.0 to 5.4 ns; `clk_sar` from 3.0 to 3.25 ns, 3.6 to 3.85 ns, and 4.2 to 4.45 ns; `res` from 6.0 to 6.6 ns; `intg` from 8.0 to 8.7 ns; `zoom` from 9.2 to 10.8 ns; `clk_zoom` from 9.2 to 9.45 ns and 9.8 to 10.05 ns; and `rst_zoom` from 11.0 to 11.5 ns. All outputs should return low between their public windows and repeat every 32 ns.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `adc_zoom_timing_sequencer.va`.
Do not add or omit artifacts.
