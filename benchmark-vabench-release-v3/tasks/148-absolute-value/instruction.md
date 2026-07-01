# Absolute Value Behavior

Implement a pure voltage-domain absolute-value DUT.

## Public Interface

Declare module `absolute_value_behavior` with positional ports `sigin, sigout`.
Both ports are electrical.

## Functional Contract

- Drive `sigout` to the absolute value of the voltage at `sigin`.
- Preserve positive input voltages unchanged.
- Reflect negative input voltages to positive output voltages with the same
  magnitude.
- The model is memoryless and deterministic.

## Modeling Constraints

Return only `absolute_value_behavior.va`. Use voltage contributions only. Do not
modify or emit the support testbench, add checker logic, hard-code private
waveform sample points, add simulator-private side channels, use current
contributions, `ddt()`, or `idt()`.
