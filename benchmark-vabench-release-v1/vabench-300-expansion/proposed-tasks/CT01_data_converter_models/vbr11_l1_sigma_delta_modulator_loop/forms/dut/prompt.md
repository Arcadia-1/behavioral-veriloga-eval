# Task: sigma_delta_modulator_loop:dut

## Release Task Contract

- Form: `dut`
- Track: `core`
- Difficulty: `D3`
- Category: Data Converter Models
- Domain: voltage-domain behavioral Verilog-A
- Score surface: `model-capability`

## Form-Specific Requirements

Implement the Verilog-A DUT artifact only. The released companion testbench and checker will drive the observable behavior.

## Output Contract

Submit `sigma_delta_modulator_loop.va`. Keep artifact names exactly as listed so the released checker can find them.

## Task-Specific Public Description

Implement the `dut` form for **First-order sigma-delta modulator loop**. The solution should preserve public interface behavior, event timing, and measurement outputs. It must not rely on transistor-level device models or hidden checker-specific constants.

## Public Behavioral Targets

- Preserve the public interface behavior, event timing, and measurement outputs described by the task.
- Stay within the voltage-domain behavioral Verilog-A subset.
- The submitted artifact should satisfy the released checker `checks.yaml` under the Spectre final-judge protocol.
