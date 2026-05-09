Given a voltage-domain DUT module named `voltage_clamp`, generate only a Spectre testbench.
Do not generate Verilog-A modules.

The DUT file will be available as `dut.va`; include it with `ahdl_include "dut.va"` and instantiate by positional ports.

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
- Provide 0.9 V `vdd` and 0 V `vss`.
- Drive `raw_level` through below-limit, in-range, and above-limit plateaus.
- Instantiate as `XDUT (raw_level vdd vss clamped_level) voltage_clamp`.
- Save plain scalar names: `raw_level`, `clamped_level`.
- Run exactly `tran tran stop=120n maxstep=500p`.

Return exactly one fenced `spectre` code block.
