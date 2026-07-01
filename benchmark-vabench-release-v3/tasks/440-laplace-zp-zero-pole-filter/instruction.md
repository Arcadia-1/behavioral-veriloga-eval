# Laplace Zp Zero Pole Filter

Implement one behavioral Verilog-A/AMS source file named `laplace_zp_zero_pole_filter.va`.

## Interface

Use the exact module interface shown in the starter file. This is a behavioral-continuous-time candidate, not part of the ordinary behavioral-event certification layer.

## Required Feature

Use laplace_zp() for zero/pole transfer modeling.

## Required Behavior

The intended model uses a voltage-domain continuous-time zero/pole transfer expression and drives behavioral voltage outputs only. Do not use `I(...)` current contributions.

Return exactly one source artifact named `laplace_zp_zero_pole_filter.va`.
