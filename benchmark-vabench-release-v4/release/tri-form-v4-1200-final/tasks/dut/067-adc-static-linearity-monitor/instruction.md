# ADC Static Linearity Monitor

## Task Contract

Implement the declared behavioral Verilog-A DUT bundle. The accompanying
`solver_contract.json` is the authoritative machine-readable contract.

## Public Verilog-A Interface

Submit exactly these artifacts and preserve their declared modules, ports, and order:

- `adc_static_linearity_monitor.va`: `adc_static_linearity_monitor`

## Public Parameter Contract

Preserve every declared public parameter, default, range, and override behavior
from `solver_contract.json`.

## Required Behavior

Satisfy every observable property:

- `P_STROBE_UPDATE`: The retained error metric updates only on rising crossings of vsample through vth and holds between strobes.
- `P_IDEAL_CODE`: At a strobe, vin is clipped to 0 through vref and mapped to the ideal three-bit bin-floor code.
- `P_OBSERVED_CODE`: At a strobe, d2 through d0 are threshold-decoded as an unsigned three-bit word with d2 as MSB and d0 as LSB.
- `P_ABSOLUTE_ERROR`: Each sampled error is the absolute difference in codes between the ideal and observed three-bit words.
- `P_MAX_RETENTION`: maxerr never decreases during a run and represents the largest sampled absolute code error seen so far.
- `P_METRIC_SCALE`: maxerr equals the retained maximum code error multiplied by lsb_out, with smoothing set by tr.

## Modeling Constraints

Follow the public modeling constraints in `solver_contract.json`. Keep the model
deterministic, portable to Spectre, and free of evaluator-specific behavior.

## Output Contract

Return exactly these submission-root-relative files: `adc_static_linearity_monitor.va`.
Do not add or omit artifacts.
