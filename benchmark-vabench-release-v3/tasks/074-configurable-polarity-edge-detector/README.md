# Configurable Polarity Edge Detector

Implement `configurable_polarity_edge_detector.va` in Verilog-A.

## Interface

```verilog
module configurable_polarity_edge_detector(sig, rise_en, pulse);
```

Inputs: `sig, rise_en`.
Outputs: `pulse`.

## Required Behavior

When `rise_en` is high, generate a short pulse after each rising edge of `sig`. When `rise_en` is low, generate a short pulse after each falling edge of `sig`. Do not pulse on the unselected edge polarity.

Use logic threshold 0.45 V for digital decisions, drive high outputs to 0.9 V and low outputs to 0 V, and use short transition edges so EVAS transient traces are stable away from switching instants.
