# Oomr String Voltage Probe

Implement one Verilog-A source file named `oomr_string_voltage_probe.va`.

## Required Feature

Use a string out-of-module reference in a voltage probe.

## Required Interface

```verilog
module oomr_string_voltage_probe(
    output electrical out
);
```

## Required Behavior

- Declare a string parameter named `sigpath` with the default value `"$root.vin"`.
- Probe the referenced voltage with `V(sigpath)`.
- Drive `out` with the probed voltage, smoothed by `transition(..., 0, 200p, 200p)`.
- Do not add ordinary electrical input ports to bypass the string OOMR probe.

Return exactly one source artifact named `oomr_string_voltage_probe.va`.
