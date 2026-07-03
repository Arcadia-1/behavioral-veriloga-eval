# Voltage Controlled Gain Amplifier

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Baseband / analog primitive variable-gain blocks
- Base function: Voltage-controlled differential gain amplifier with unipolar output range
- Domain: `voltage`
- Target artifact(s): `voltage_controlled_gain_amplifier.va`
- Visible context: public task, module interface, control/input roles, offset, and limiting contract.
- Evaluator boundary: validation logic is external; do not generate checker, testbench, or measurement helper artifacts.

## Public Verilog-A Interface

`voltage_controlled_gain_amplifier.va` must declare:

```verilog
module voltage_controlled_gain_amplifier(vin_p, vin_n, vctrl_p, vctrl_n, vout);
input vin_p, vin_n, vctrl_p, vctrl_n;
output vout;
electrical vin_p, vin_n, vctrl_p, vctrl_n, vout;
```

## Behavioral Contract

Model a voltage-controlled gain block. The differential control voltage `V(vctrl_p, vctrl_n)` scales the differential input after subtracting a 0.05 V input-referred offset. Use a gain constant of 1.5, center the output around 0.5 V, and clamp the final output target to the unipolar range 0.1 V through 0.9 V.

Compute the limited target as a real variable and drive `vout` with a single voltage contribution. Do not use current contributions, transistor devices, filtering, or testbench-specific constants.

## Output Contract

Return exactly one source artifact named `voltage_controlled_gain_amplifier.va`.
Do not include explanatory prose outside the source artifact contents.
