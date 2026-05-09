Write a pure Verilog-A module named `voltage_clamp` and a minimal Spectre testbench.
Return two files: `dut.va` and `tb_ref.scs`.

Core function: voltage clamp.
Behavioral intent: model a bounded analog transfer that follows the input in the middle range and clamps outside public lower/upper limits.

Public interface:
- Module name: `voltage_clamp`.
- Inputs: `raw_level`, `vdd`, `vss`.
- Output: `clamped_level`.
- Public real parameters: `vlo=0.18`, `vhi=0.72`, `tr=40p`.

Compatibility requirements:
- Use voltage-domain electrical ports only.
- Be compatible with real Cadence Spectre.
- Declare port direction and electrical discipline separately.
- Drive output targets with `transition(...)`.
- Do not use current contributions, `ddt()`, or `idt()`.

Public evaluation contract:
- The checker reads public waveform columns `raw_level` and `clamped_level`.
- The fixed testbench exercises below-limit, in-range, and above-limit input regions.
- The fixed harness runs exactly `tran tran stop=120n maxstep=500p`.


Testbench requirements:
- Start with `simulator lang=spectre` and `global 0`.
- Include `dut.va` with `ahdl_include`.
- Instantiate `voltage_clamp` by positional ports: `(raw_level vdd vss clamped_level)`.
- Drive `raw_level` through below-limit, in-range, and above-limit plateaus.
- Save plain scalar names: `raw_level`, `clamped_level`.
- Run exactly `tran tran stop=120n maxstep=500p`.
