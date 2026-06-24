# Event Counter Windowed 16b

Implement `event_counter_windowed_16b.va` in Verilog-A.

## Interface

```verilog
module event_counter_windowed_16b(gate, event, done, count0, count1, count2, count3, count4, count5, count6, count7, count8, count9, count10, count11, count12, count13, count14, count15);
```

Inputs: `gate, event`.
Outputs: `done, count0, count1, count2, count3, count4, count5, count6, count7, count8, count9, count10, count11, count12, count13, count14, count15`.

## Required Behavior

Count rising edges on `event` only while `gate` is high. Clear the count on each rising `gate`; after falling `gate`, hold the count and assert `done`.

Use logic threshold 0.45 V for digital decisions, drive high outputs to 0.9 V and low outputs to 0 V, and use short transition edges so EVAS transient traces are stable away from switching instants.
