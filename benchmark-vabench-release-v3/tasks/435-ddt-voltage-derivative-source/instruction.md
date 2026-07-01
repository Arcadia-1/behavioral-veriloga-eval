# Ddt Voltage Derivative Source

Implement one behavioral Verilog-A/AMS source file named `ddt_voltage_derivative_source.va`.

## Interface

Use the exact module interface shown in the starter file. This is a behavioral-continuous-time candidate, not part of the ordinary behavioral-event certification layer.

## Required Feature

Use ddt() to form a voltage-domain derivative source.

## Required Behavior

The intended model samples a voltage-domain derivative expression and drives behavioral voltage outputs only. Do not use `I(...)` current contributions.

Return exactly one source artifact named `ddt_voltage_derivative_source.va`.
