# Low Active Enable Decoder 4b

Implement `low_active_enable_decoder_4b.va` in Verilog-A.

## Interface

```verilog
module low_active_enable_decoder_4b(en_n, a0, a1, a2, a3, y0_n, y1_n, y2_n, y3_n, y4_n, y5_n, y6_n, y7_n, y8_n, y9_n, y10_n, y11_n, y12_n, y13_n, y14_n, y15_n);
```

Inputs: `en_n, a0, a1, a2, a3`.
Outputs: `y0_n, y1_n, y2_n, y3_n, y4_n, y5_n, y6_n, y7_n, y8_n, y9_n, y10_n, y11_n, y12_n, y13_n, y14_n, y15_n`.

## Required Behavior

When `en_n` is low, exactly one active-low output `yN_n` must be low, where `N` is the unsigned value of `a[3:0]`. When `en_n` is high, all outputs must be high.

Use logic threshold 0.45 V for digital decisions, drive high outputs to 0.9 V and low outputs to 0 V, and use short transition edges so EVAS transient traces are stable away from switching instants.
