# DAC Mismatch Unit Weighting Model

Implement a bounded 4-bit DAC with explicit nonideal unit weights.

## Public Interface

Declare module `dac_mismatch_unit_weighting_model` with positional ports `b0,
b1, b2, b3, out`. All ports are electrical.

## Public Parameter Contract

Provide these overrideable public parameters:

- `vhi = 0.9 V`: high endpoint of the reconstructed output range.
- `vlo = 0.0 V`: low endpoint of the reconstructed output range.
- `tr = 100 ps`: output transition smoothing time.

Use a 0.45 V logic threshold for each input bit.

## Functional Contract

Treat `b0..b3` as voltage-coded control bits. Reconstruct the DAC output from
explicit nonideal weights 1.00, 2.02, 3.96, and 8.08, normalized by the
all-active weight sum. Drive `out` between `vlo` and `vhi`; the all-zero input
maps to `vlo` and the all-active input maps to `vhi`.

## Modeling Constraints

Return only `dac_mismatch_unit_weighting_model.va`. Use deterministic
voltage-domain Verilog-A and smooth output transitions. Do not modify or emit
the support testbench, add checker logic, hard-code private waveform sample
points, add simulator-private side channels, use current contributions,
`ddt()`, or `idt()`.
