# Soft Voltage Clamp

Implement `soft_voltage_clamp_behavior` in `soft_voltage_clamp_behavior.va`.

The module is a voltage-domain DUT with port order `vin, vout, vgnd`. Declare
all ports as `electrical`; `vin` and `vgnd` are inputs and `vout` is the output.

Use `vgnd` as the voltage reference. Pass `V(vin, vgnd)` through in the linear
region from 0.0 V to 0.4 V, including the knee points. Below 0.0 V, apply an
exponential soft lower limit that approaches -0.2 V asymptotically. Above
0.4 V, apply an exponential soft upper limit that approaches 0.6 V
asymptotically. Use a 0.2 V softness span on both sides.

The response should be continuous, monotonic, and soft-limited rather than
hard-clipped at the asymptotes.
