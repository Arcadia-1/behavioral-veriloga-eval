Implement a supply-referenced limiter named `limiter_rails` with port order `vdd, vss, vin, vmax, vmin, vout`. Clamp above `V(vdd)-V(vmax)` and below `V(vss)+V(vmin)`; otherwise pass `vin`.
