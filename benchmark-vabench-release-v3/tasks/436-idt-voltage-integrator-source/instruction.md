# Idt Voltage Integrator Source

Implement one behavioral Verilog-A/AMS source file named `idt_voltage_integrator_source.va`.

## Interface

Use the exact module interface shown in the starter file. This is a behavioral-continuous-time candidate, not part of the ordinary behavioral-event certification layer.

## Required Feature

Use idt() to form a voltage-domain integrator source.

## Required Behavior

The intended model samples a voltage-domain integral expression and drives behavioral voltage outputs only. Do not use `I(...)` current contributions.

Return exactly one source artifact named `idt_voltage_integrator_source.va`.
