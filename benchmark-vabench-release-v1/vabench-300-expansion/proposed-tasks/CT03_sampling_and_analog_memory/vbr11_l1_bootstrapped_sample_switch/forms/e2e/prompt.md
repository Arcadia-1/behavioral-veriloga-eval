# Task: bootstrapped_sample_switch:e2e

## Release Task Contract

- Form: `e2e`
- Track: `core`
- Difficulty: `D2`
- Category: Sampling and Analog Memory
- Domain: voltage-domain behavioral Verilog-A
- Score surface: `model-capability`

## Form-Specific Requirements

Implement the complete DUT plus Spectre testbench artifact set needed to run the end-to-end behavior check.

## Output Contract

Submit `bootstrapped_sample_switch.va`, `tb_bootstrapped_sample_switch.scs`. Keep artifact names exactly as listed so the released checker can find them.

## Task-Specific Public Description

Implement the `e2e` form for **Bootstrapped sample switch abstraction**. The solution should preserve public interface behavior, event timing, and measurement outputs. It must not rely on transistor-level device models or hidden checker-specific constants.

## Public Behavioral Targets

- Preserve the public interface behavior, event timing, and measurement outputs described by the task.
- Stay within the voltage-domain behavioral Verilog-A subset.
- The submitted artifact should satisfy the released checker `checks.yaml` under the Spectre final-judge protocol.
