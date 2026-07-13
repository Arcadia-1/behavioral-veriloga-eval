# ADC Static Linearity Monitor Bugfix

## Task Contract

The supplied Verilog-A system violates its public circuit contract. Repair the
complete editable bundle.
The accompanying `solver_contract.json` is the authoritative structured contract.

## Public Verilog-A Interface

Preserve the exact declared artifact set, module graph, ports, and dependencies:

- `adc_static_linearity_monitor.va`: `adc_static_linearity_monitor`

## Public Parameter Contract

Preserve every public parameter declaration and override behavior in
`solver_contract.json`.

## Required Behavior

The repaired bundle must satisfy every public property:

- `P_STROBE_UPDATE`: The retained error metric updates only on rising crossings of vsample through vth and holds between strobes.
- `P_IDEAL_CODE`: At a strobe, vin is clipped to 0 through vref and mapped to the ideal three-bit bin-floor code.
- `P_OBSERVED_CODE`: At a strobe, d2 through d0 are threshold-decoded as an unsigned three-bit word with d2 as MSB and d0 as LSB.
- `P_ABSOLUTE_ERROR`: Each sampled error is the absolute difference in codes between the ideal and observed three-bit words.
- `P_MAX_RETENTION`: maxerr never decreases during a run and represents the largest sampled absolute code error seen so far.
- `P_METRIC_SCALE`: maxerr equals the retained maximum code error multiplied by lsb_out, with smoothing set by tr.

## Modeling Constraints

- Follow the public modeling constraints in `solver_contract.json`.
- Preserve the exact file set, module graph, ports, parameters, and public traces.
- Do not add debug outputs, validation state, side channels, or stimulus-specific fixes.

## Output Contract

Return the repaired bundle with exactly these submission-root-relative paths: `adc_static_linearity_monitor.va`.
Every supplied `.va` file is editable; do not add or omit files.
