from __future__ import annotations

from runners.vabench_release_prompt_wrapper import (
    RELEASE_RUNNER_WRAPPER_VERSION,
    build_release_generation_prompt,
    extract_marked_artifacts,
)


def test_release_prompt_wrapper_keeps_runner_protocol_outside_public_prompt() -> None:
    public_prompt = "# Task: demo\n\n## Output Contract\n\nReturn exactly one source artifact named `demo.va`."

    wrapped = build_release_generation_prompt(
        public_prompt=public_prompt,
        target_artifacts=["demo.va"],
        form="dut",
    )

    assert RELEASE_RUNNER_WRAPPER_VERSION in wrapped
    assert "\nQuestion:\n" in wrapped
    assert public_prompt in wrapped
    assert "\nEVAS/Spectre compatibility rules:\n" in wrapped
    assert '`include "disciplines.vams"' in wrapped
    assert "while (1) or forever" in wrapped
    assert "PWL vector spans multiple lines" in wrapped
    assert "\nAnswer:\n" in wrapped
    assert "[BEGIN file: demo.va]" in wrapped
    assert "[DONE file: demo.va]" in wrapped
    assert "These are public language, artifact, and simulator compatibility rules" in wrapped


def test_marked_artifact_extraction_uses_exact_target_names() -> None:
    response = """\
[BEGIN file: demo.va]
```verilog-a
`include "constants.vams"
`include "disciplines.vams"
module demo(out);
  output out;
  electrical out;
  analog begin
    V(out) <+ 0.5;
  end
endmodule
```
[DONE file: demo.va]

[BEGIN file: tb_demo.scs]
```spectre
simulator lang=spectre
global 0
ahdl_include "demo.va"
Xdut (out) demo
tran tran stop=1n
save out
```
[DONE file: tb_demo.scs]
"""

    artifacts = extract_marked_artifacts(response)

    assert sorted(artifacts) == ["demo.va", "tb_demo.scs"]
    assert artifacts["demo.va"].startswith('`include "constants.vams"')
    assert artifacts["tb_demo.scs"].startswith("simulator lang=spectre")
    assert "```" not in artifacts["demo.va"]
    assert "[DONE file" not in artifacts["tb_demo.scs"]
