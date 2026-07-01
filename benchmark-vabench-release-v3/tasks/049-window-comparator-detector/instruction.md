# Window Comparator Detector

Implement `window_comparator_ref.va` in Verilog-A.

## Public Interface

Declare module `window_comparator_ref(VDD, VSS, vin, out)` with scalar
electrical voltage-domain ports. `VDD` and `VSS` are supply rails, `vin` is the
input waveform, and `out` is the in-window decision output.

## Public Parameter Contract

- `vlow`: lower window threshold, default `0.3`.
- `vhigh`: upper window threshold, default `0.6`.
- `tedge`: output transition smoothing time, default `200p`.

## Functional Contract

- Drive `out` high only when `vlow < V(vin, VSS) < vhigh`.
- Drive `out` low when `V(vin, VSS) <= vlow` or `V(vin, VSS) >= vhigh`.
- Initialize the decision from the initial input voltage.
- Resolve both rising and falling crossings of the lower and upper thresholds.
- Drive `out` rail-to-rail relative to `VDD` and `VSS` using a smoothed
  voltage-domain transition.

## Modeling Constraints

Return only `window_comparator_ref.va`. Do not emit a Spectre testbench,
checker logic, private test hooks, or simulator-private side channels. Use
voltage contributions only; do not use transistor-level devices, current
contributions, `ddt()`, or `idt()`.
