# XOR Phase Detector

Implement `xor_phase_detector.va` in Verilog-A.

## Interface

```verilog
module xor_phase_detector(
    input  electrical ref,
    input  electrical fb,
    output electrical up,
    output electrical down
);
```

## Required Behavior

This task asks for the `xor_phase_detector` behavioral DUT module, not a
Spectre testbench. The module is a combinational XOR-style phase detector for
voltage-coded clocks.

Support this public parameter and legal override:

| Parameter | Default | Unit / range | Contract |
| --- | ---: | --- | --- |
| `vdd` | `1.2` | V, `(0:inf)` | High level for voltage-coded outputs and threshold reference. |

Required observable behavior:

- Interpret `ref` and `fb` logic levels using a threshold of `vdd / 2`.
- Drive `up` high when the interpreted `ref` and `fb` levels differ.
- Drive `down` high when the interpreted `ref` and `fb` levels match.
- Update outputs combinationally from the current input voltages.
- Drive outputs as 0 V / `vdd` voltage-coded signals.

Use voltage contributions only. Do not use current contributions,
transistor-level devices, AC/noise analysis, checker logic, private test hooks,
or simulator-private side channels.

## Output

Return exactly one source artifact named `xor_phase_detector.va`.
