# Settling Window Detector

Implement `settling_window_detector.va` in Verilog-A.

## Interface

```verilog
module settling_window_detector(vin, target, tol, settled, t_code0, t_code1, t_code2, t_code3, t_code4, t_code5, t_code6, t_code7);
```

Inputs: `vin, target, tol`.
Outputs: `settled, t_code0, t_code1, t_code2, t_code3, t_code4, t_code5, t_code6, t_code7`.

## Required Behavior

Assert `settled` only after `vin` has stayed within `target +/- tol` continuously for at least 20 ns. Reset the hold timer whenever `vin` leaves the window. Report the 1 ns code for the current in-window entry time on `t_code[7:0]`.

Use logic threshold 0.45 V for digital decisions, drive high outputs to 0.9 V and low outputs to 0 V, and use short transition edges so EVAS transient traces are stable away from switching instants.
