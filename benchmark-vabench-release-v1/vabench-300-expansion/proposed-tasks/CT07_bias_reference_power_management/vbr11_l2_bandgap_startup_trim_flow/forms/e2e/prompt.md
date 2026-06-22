# Task: bandgap_startup_trim:e2e

## Release Task Contract

- Form: `e2e`
- Track: `core`
- Difficulty: `D3`
- Category: Bias Reference and Power Management
- Domain: voltage-domain behavioral Verilog-A
- Score surface: `model-capability`

## Form-Specific Requirements

Implement the complete DUT plus Spectre testbench artifact set needed to run the end-to-end behavior check.

## Output Contract

Submit `bandgap_startup_trim.va`, `tb_bandgap_startup_trim.scs`. Keep artifact names exactly as listed so the released checker can find them.

## Task-Specific Public Description

Implement the `e2e` form for **Bandgap startup and trim convergence flow**. The solution should preserve public interface behavior, event timing, and measurement outputs. It must not rely on transistor-level device models or hidden checker-specific constants.

## Public Behavioral Targets

- Preserve the public interface behavior, event timing, and measurement outputs described by the task.
- Stay within the voltage-domain behavioral Verilog-A subset.
- The submitted artifact should satisfy the released checker `checks.yaml` under the Spectre final-judge protocol.
