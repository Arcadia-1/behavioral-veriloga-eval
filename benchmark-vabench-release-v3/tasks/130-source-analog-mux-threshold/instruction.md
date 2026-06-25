Implement a threshold-controlled analog mux.

The module must be named `analog_mux_threshold` and use this port order:

`vin1, vin2, vsel, vout`

When `vsel` is above `vth`, pass `vin1` to `vout`; otherwise pass `vin2`. The
selection state should update on both rising and falling threshold crossings.
