# Laplace Np Pole Filter

Implement one behavioral Verilog-A/AMS source file named `laplace_np_pole_filter.va`.

## Interface

Use the exact module interface shown in the starter file. This is a behavioral-continuous-time candidate, not part of the ordinary behavioral-event certification layer.

## Required Feature

Use laplace_np() for pole-form continuous-time transfer modeling.

## Required Behavior

The intended model uses a voltage-domain continuous-time pole-form transfer expression and drives behavioral voltage outputs only. Do not use `I(...)` current contributions.

Return exactly one source artifact named `laplace_np_pole_filter.va`.
