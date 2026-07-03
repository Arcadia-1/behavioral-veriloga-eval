# Hard Voltage Clamp

Implement `hard_voltage_clamp_behavior` in `hard_voltage_clamp_behavior.va`.

The module is a voltage-domain DUT with port order `vin, vout, vgnd`. Declare
all ports as `electrical`; `vin` and `vgnd` are inputs and `vout` is the output.

Use `vgnd` as the voltage reference. When `V(vin, vgnd)` is inside the clamp
range, including both rails, pass it through to `V(vout, vgnd)`. Below the
lower rail, drive the lower clamp voltage. Above the upper rail, drive the upper
clamp voltage.

Provide overridable real parameters `vclamp_lower=0` and `vclamp_upper=1`, in
volts, and use the instance-provided values when they are overridden.
