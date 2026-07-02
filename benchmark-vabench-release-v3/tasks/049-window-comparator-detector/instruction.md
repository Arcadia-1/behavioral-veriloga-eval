# Window Comparator Detector

Implement a voltage-domain window comparator detector.

## Public Interface

Declare module `window_comparator_ref` with positional ports `VDD, VSS, vin,
out`. All ports are electrical. `VDD` and `VSS` are supply rails, `vin` is the
input voltage, and `out` is the in-window decision output.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vlow = 0.3 V`: lower window threshold.
- `vhigh = 0.6 V`: upper window threshold.
- `tedge = 200p`: output transition smoothing time.

## Functional Contract

- Initialize the decision from the initial input voltage.
- Drive `out` high only while `vlow < V(vin,VSS) < vhigh`.
- Drive `out` low when `V(vin,VSS) <= vlow` or `V(vin,VSS) >= vhigh`.
- Resolve crossings of both the lower and upper thresholds in both directions.
- Drive `out` rail-to-rail relative to `VDD` and `VSS` using finite
  transition-style smoothing.

## Modeling Constraints

Return only `window_comparator_ref.va`. Use voltage contributions only. Do not
modify or emit the support testbench, add checker logic, hard-code waveform
sample points, add simulator-private side channels, use transistor-level
devices, current contributions, `ddt()`, or `idt()`. Update retained in-window
state at threshold-crossing events and drive the output contribution outside
those event blocks.
