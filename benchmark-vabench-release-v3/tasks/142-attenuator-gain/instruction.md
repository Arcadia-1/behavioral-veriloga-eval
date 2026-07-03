# Attenuator Gain

## Task Contract

- Form: `dut`
- Level: `L1`
- Category: Baseband / analog primitive gain blocks
- Base function: Voltage-domain attenuator with dB gain control
- Domain: `voltage`
- Target artifact(s): `attenuator_gain.va`
- Visible context: public task, module interface, parameters, and behavioral contract.
- Evaluator boundary: validation logic is external; do not generate checker, testbench, or measurement helper artifacts.

## Public Verilog-A Interface

`attenuator_gain.va` must declare:

```verilog
module attenuator_gain(vin, vout);
input vin;
output vout;
electrical vin, vout;
parameter real attenuation = 0;
```

## Behavioral Contract

Implement a continuous voltage attenuator. The `attenuation` parameter is in dB and controls the amplitude ratio. A 0 dB setting passes the input unchanged; positive attenuation reduces the output amplitude using the standard voltage dB relationship.

Drive `vout` as a voltage-domain output proportional to `vin`. Use Verilog-A real arithmetic and math operators for the dB-to-linear conversion. Do not use current contributions, transistor devices, or testbench-specific constants.

## Output Contract

Return exactly one source artifact named `attenuator_gain.va`.
Do not include explanatory prose outside the source artifact contents.
