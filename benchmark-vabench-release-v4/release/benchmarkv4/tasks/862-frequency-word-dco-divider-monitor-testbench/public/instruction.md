# Frequency-word DCO with Divider Monitor Testbench

## Task Contract

Write one top-level Spectre testbench that verifies the public contract of the
supplied read-only `Frequency-word DCO with Divider Monitor` DUT. The evaluator runs the same submitted bytes
against the correct DUT and five anonymous semantic negative DUTs. Your
testbench must accept the correct DUT and expose all five behavioral faults.

## Public Verilog-A Interface

- Artifact `frequency_word_dco.va`:
  - Module `frequency_word_dco` (entry)
    - position 0: `enable` (input, electrical)
    - position 1: `rst` (input, electrical)
    - position 2: `fcw_5` (input, electrical)
    - position 3: `fcw_4` (input, electrical)
    - position 4: `fcw_3` (input, electrical)
    - position 5: `fcw_2` (input, electrical)
    - position 6: `fcw_1` (input, electrical)
    - position 7: `fcw_0` (input, electrical)
    - position 8: `dco_clk` (output, electrical)
    - position 9: `div_clk` (output, electrical)
    - position 10: `freq_metric` (output, electrical)

Stable public Spectre binding:

The submitted `testbench.scs` must use the supplied DUT through this public binding:

- Include path: `./dut/frequency_word_dco.va`
- DUT instance: `XDUT (enable rst fcw_5 fcw_4 fcw_3 fcw_2 fcw_1 fcw_0 dco_clk div_clk freq_metric) frequency_word_dco`
- Required saved public traces: `enable`, `rst`, `fcw_5`, `fcw_4`, `fcw_3`, `fcw_2`, `fcw_1`, `fcw_0`, `dco_clk`, `div_clk`, `freq_metric`
- Use one bounded transient analysis with a finite positive stop time.

You must design the stimulus yourself. Save traces as bare public signal names
(for example `clk`, not suffixed or hierarchical forms such as `clk:V` or
`XDUT.clk`). Do not redefine the DUT, drive DUT output nets, save
hierarchical/private nodes, or use checker/gold/internal files.

## Public Parameter Contract

- `frequency_word_dco.vdd` defaults to `0.9`; valid range: declared Verilog-A parameter constraint or finite portable value; overrides public vdd behavior for module frequency_word_dco.
- `frequency_word_dco.vss` defaults to `0.0`; valid range: declared Verilog-A parameter constraint or finite portable value; overrides public vss behavior for module frequency_word_dco.
- `frequency_word_dco.vth` defaults to `0.45`; valid range: declared Verilog-A parameter constraint or finite portable value; overrides public vth behavior for module frequency_word_dco.
- `frequency_word_dco.f_min` defaults to `80.0e6` Hz; valid range: declared Verilog-A parameter constraint or finite portable value; overrides public f_min behavior for module frequency_word_dco.
- `frequency_word_dco.f_step` defaults to `2.0e6` Hz; valid range: declared Verilog-A parameter constraint or finite portable value; overrides public f_step behavior for module frequency_word_dco.
- `frequency_word_dco.f_max` defaults to `250.0e6` Hz; valid range: declared Verilog-A parameter constraint or finite portable value; overrides public f_max behavior for module frequency_word_dco.
- `frequency_word_dco.divide_ratio` defaults to `4 from [1:inf)`; valid range: declared Verilog-A parameter constraint or finite portable value; overrides public divide_ratio behavior for module frequency_word_dco.
- `frequency_word_dco.tr` defaults to `100p from (0:inf)` s; valid range: declared Verilog-A parameter constraint or finite portable value; overrides public tr behavior for module frequency_word_dco.

## Required Behavior

Create stimulus and save traces sufficient for the fixed evaluator oracle to check:

- `P_RESET_DISABLE_STOP`: exercise and make observable: Reset or disabled operation stops and clears both clocks, the divider counter, and the frequency metric. Required traces: `time`, `enable`, `rst`, `dco_clk`, `div_clk`, `freq_metric`.
- `P_FREQUENCY_WORD_MAPPING`: exercise and make observable: The six-bit frequency word maps to min(f_max, f_min plus f_step times code), with the public normalized metric matching that target. Required traces: `time`, `fcw_5`, `fcw_4`, `fcw_3`, `fcw_2`, `fcw_1`, `fcw_0`, `dco_clk`, `freq_metric`.
- `P_DIVIDER_MONITOR`: exercise and make observable: div_clk toggles once per divide_ratio rising DCO edges and its counter restarts after reset or disable. Required traces: `time`, `enable`, `rst`, `dco_clk`, `div_clk`.
- `P_RESTART_MONOTONICITY`: exercise and make observable: Enable restarts both clocks low with the first DCO rise one half-period later, and larger frequency words produce nondecreasing edge counts. Required traces: `time`, `enable`, `rst`, `fcw_5`, `fcw_4`, `fcw_3`, `fcw_2`, `fcw_1`, `fcw_0`, `dco_clk`, `div_clk`.

The required trace names are: `time`, `enable`, `rst`, `fcw_5`, `fcw_4`, `fcw_3`, `fcw_2`, `fcw_1`, `fcw_0`, `dco_clk`, `div_clk`, `freq_metric`.

## Modeling Constraints

- Submit one self-contained top-level transient `.scs` file.
- Use only the declared `./dut/...` source paths and public DUT interfaces.
- Do not redefine the DUT, drive declared DUT outputs, inspect private internals,
  access undeclared files, or emit a self-reported result.
- Missing traces, setup errors, and invalid runs do not count as behavioral kills.

## Output Contract

Return exactly one artifact named `testbench.scs`. Do not return a DUT,
checker, script, data file, waveform, or auxiliary deck.
