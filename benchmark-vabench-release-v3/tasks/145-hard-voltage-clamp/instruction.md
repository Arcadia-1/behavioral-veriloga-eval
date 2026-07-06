# Hard Voltage Clamp

## Task Contract

Implement the requested Verilog-A artifact for `Hard Voltage Clamp`.
- Form: `dut`
- Level: `L1`
- Category: `mixed_signal`
- Target artifact(s): `hard_voltage_clamp_behavior.va`

Implement `hard_voltage_clamp_behavior` in `hard_voltage_clamp_behavior.va`.

The module is a voltage-domain DUT with port order `vin, vout, vgnd`. Declare
all ports as `electrical`; `vin` and `vgnd` are inputs and `vout` is the output.

Use `vgnd` as the voltage reference. When `V(vin, vgnd)` is inside the clamp
range, including both rails, pass it through to `V(vout, vgnd)`. Below the
lower rail, drive the lower clamp voltage. Above the upper rail, drive the upper
clamp voltage.

Provide overridable real parameters `vclamp_lower=0` and `vclamp_upper=1`, in
volts, and use the instance-provided values when they are overridden.

## Public Verilog-A Interface

The file `hard_voltage_clamp_behavior.va` must define `module hard_voltage_clamp_behavior(vin, vout, vgnd);`. All ports are electrical. `vin` is the input, `vgnd` is the local reference, and `vout` is the clamped referenced output.

## Public Parameter Contract

The public parameters declared by `hard_voltage_clamp_behavior.va` are part of the contract and may be overridden by validation harnesses:

- `parameter real vclamp_upper = 1;`
- `parameter real vclamp_lower = 0;`

## Required Behavior

Use `vgnd` as the local voltage reference. When `V(vin, vgnd)` is between `vclamp_lower` and `vclamp_upper`, including both rails, pass that referenced voltage through to `V(vout, vgnd)`. Below the lower rail, drive the lower clamp value; above the upper rail, drive the upper clamp value.

## Modeling Constraints

Use deterministic Verilog-A behavioral modeling appropriate for the public circuit contract. The visible testbench is a public validation scenario; do not hard-code a particular stimulus table, transient stop time, or validation sample window into the DUT unless that behavior is part of the public circuit contract.

## Output Contract

Return exactly one complete source artifact named `hard_voltage_clamp_behavior.va`. Do not include explanatory prose outside the source artifact contents.
