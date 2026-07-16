from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    ROOT
    / "benchmark-vabench-release-v4"
    / "provenance"
    / "dut-base-v3-exact-five-hash-bound-v2"
)
RELEASE = ROOT / "benchmark-vabench-release-v4" / "release" / "benchmarkv4"


def _family(prefix: str) -> Path:
    matches = list(SOURCE.glob(f"{prefix}-*"))
    assert len(matches) == 1
    return matches[0]


def _spec(prefix: str) -> dict[str, object]:
    return json.loads((_family(prefix) / "evaluator" / "family_spec.json").read_text())


def _task(name: str) -> Path:
    task = RELEASE / "tasks" / name
    assert task.is_dir()
    return task


def _public_contract(task_name: str) -> dict[str, object]:
    return json.loads((_task(task_name) / "public_contract.json").read_text())


def _binding_nets(task_name: str) -> dict[str, str]:
    contract = _public_contract(task_name)
    nets: dict[str, str] = {}
    for instance in contract["testbench_binding"]["instances"]:
        for connection in instance["connections"]:
            nets[connection["port_ref"]] = connection["net"]
    return nets


def test_masked_config_public_binding_uses_its_declared_trace_net_names() -> None:
    spec = _spec("058")
    instance = spec["testbench_binding"]["instances"][0]
    nets = {item["port_ref"]: item["net"] for item in instance["connections"]}
    for bit in range(32):
        assert nets[f"old_cfg[{bit}]"] == f"old{bit}"
        assert nets[f"new_cfg[{bit}]"] == f"new{bit}"
        assert nets[f"mask[{bit}]"] == f"mask{bit}"
        assert nets[f"out_cfg[{bit}]"] == f"out{bit}"


def test_control_word_public_binding_declares_both_parameterized_instances() -> None:
    spec = _spec("147")
    instances = spec["testbench_binding"]["instances"]
    assert {item["name"] for item in instances} == {"XCTRL42", "XCTRL85"}
    for instance in instances:
        ctrl = int(instance["parameter_overrides"]["ctrl"])
        assert ctrl in {42, 85}
        assert {
            item["port_ref"]: item["net"] for item in instance["connections"]
        } == {f"d{bit}": f"d{bit}_{ctrl}" for bit in range(7)}


def test_repaired_families_have_explicit_reference_testbenches() -> None:
    for prefix in (
        "013",
        "017",
        "020",
        "021",
        "022",
        "024",
        "028",
        "030",
        "033",
        "034",
        "037",
        "040",
        "041",
        "042",
        "043",
        "044",
        "046",
        "050",
        "051",
        "052",
        "053",
        "054",
        "055",
        "056",
        "057",
        "058",
        "059",
        "060",
        "062",
        "064",
        "065",
        "066",
        "067",
        "071",
        "073",
        "074",
        "076",
        "077",
        "078",
        "102",
        "109",
        "111",
        "147",
        "170",
        "301",
        "302",
        "321",
        "364",
        "398",
    ):
        reference = _family(prefix) / "evaluator" / "reference_tb.scs"
        text = reference.read_text(encoding="utf-8")
        assert re.search(r'ahdl_include\s+"\./dut/[^\"]+\.va"', text)


def test_strengthened_reference_testbenches_cover_previous_survivors() -> None:
    strongarm = (
        _family("017") / "evaluator" / "reference_tb.scs"
    ).read_text(encoding="utf-8")
    assert "4.30n  0.450" in strongarm
    assert "tran tran stop=5n" in strongarm

    sample_hold = (
        _family("024") / "evaluator" / "reference_tb.scs"
    ).read_text(encoding="utf-8")
    assert "4.0n    0.78" in sample_hold
    assert "24.0n   0.22" in sample_hold
    assert "tran tran stop=1u maxstep=1n" in sample_hold


def test_charge_pump_reference_never_drives_a_declared_dut_output() -> None:
    family = _family("321")
    spec = json.loads((family / "evaluator" / "family_spec.json").read_text())
    output_nets = {
        connection["net"]
        for instance in spec["testbench_binding"]["instances"]
        for connection in instance["connections"]
        if connection["port_ref"] in {"vctrl", "imbalance_metric", "balanced"}
    }
    text = (family / "evaluator" / "reference_tb.scs").read_text(encoding="utf-8")
    driven_nets = {
        match.group(1)
        for match in re.finditer(
            r"^\s*[A-Za-z_][A-Za-z0-9_]*\s+\(\s*([A-Za-z_][A-Za-z0-9_]*)\s+0\s*\)\s+vsource\b",
            text,
            re.MULTILINE | re.IGNORECASE,
        )
    }
    assert output_nets.isdisjoint(driven_nets)


def test_release_testbench_includes_use_declared_dut_path_contract() -> None:
    bad_includes: list[tuple[str, str]] = []
    missing_support: list[tuple[str, str]] = []
    for task in sorted((RELEASE / "tasks").glob("*-testbench")):
        reference = task / "evaluator" / "reference_tb.scs"
        if not reference.exists():
            reference = task / "evaluator" / "score_tb.scs"
        text = reference.read_text()
        for match in re.finditer(r'ahdl_include\s+"([^"]+)"', text):
            include_path = match.group(1)
            if not include_path.startswith("./dut/"):
                bad_includes.append((task.name, include_path))
            if include_path.startswith("./dut/support/"):
                public_support = (
                    task / "public" / "supplied_dut" / include_path.removeprefix("./dut/")
                )
                if not public_support.exists():
                    missing_support.append((task.name, include_path))

    assert bad_includes == []
    assert missing_support == []


def test_release_reference_decks_do_not_drive_declared_outputs() -> None:
    direct_drives: list[tuple[str, str]] = []
    for task in sorted((RELEASE / "tasks").glob("*-testbench")):
        reference = task / "evaluator" / "reference_tb.scs"
        if not reference.exists():
            reference = task / "evaluator" / "score_tb.scs"
        text = reference.read_text()
        contract = json.loads((task / "public_contract.json").read_text())
        port_directions: dict[str, dict[str, str]] = {}
        for file_contract in contract["artifact_contract"]["files"]:
            for module in file_contract["modules"]:
                module_ports: dict[str, str] = {}
                for port in module["ports"]:
                    module_ports[port["name"]] = port["direction"]
                    module_ports[port["name"].split("[", 1)[0]] = port["direction"]
                port_directions[module["name"]] = module_ports

        output_nets: set[str] = set()
        for instance in contract["testbench_binding"]["instances"]:
            module_ports = port_directions[instance["module_ref"]]
            for connection in instance["connections"]:
                port_ref = connection["port_ref"]
                direction = module_ports.get(
                    port_ref,
                    module_ports.get(port_ref.split("[", 1)[0]),
                )
                net = connection["net"]
                if direction == "output" and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", net):
                    output_nets.add(net)

        for net in output_nets:
            if re.search(
                rf"^V\w+\s*\([^)]*\b{re.escape(net)}\b[^)]*\)\s+vsource\b",
                text,
                re.MULTILINE,
            ):
                direct_drives.append((task.name, net))

    assert direct_drives == []


def test_sarfend_public_contract_exposes_trial_and_bit_mapping_semantics() -> None:
    task_names = (
        "186-sarfend-logic-4b",
        "686-sarfend-logic-4b-testbench",
        "1186-sarfend-logic-4b-bugfix",
    )
    for task_name in task_names:
        task = _task(task_name)
        instruction = (task / "public" / "instruction.md").read_text()
        assert "dp4=dm4=0" in instruction
        assert "dp3=dm3=dp2=dm2=dp1=dm1=1" in instruction
        assert "dout3=dp4" in instruction
        assert "`dtest3`, `dtest2`, `dtest1`, then `dtest0`" in instruction

        properties = {
            item["id"]: item["observable_contract"]
            for item in _public_contract(task_name)["properties"]
        }
        assert "dp4=dm4=0" in properties["P_CONVERSION_RESET_AND_PREVIOUS_WORD"]
        assert "MSB-to-LSB" in properties["P_SAMPLE_AND_COMPARATOR_DECISIONS"]


def test_rail_normalized_mapper_exposes_formula_and_distinct_valid_gate() -> None:
    task_names = (
        "274-rail-normalized-metric-mapper",
        "774-rail-normalized-metric-mapper-testbench",
        "1274-rail-normalized-metric-mapper-bugfix",
    )
    for task_name in task_names:
        task = _task(task_name)
        instruction = (task / "public" / "instruction.md").read_text()
        assert "local_meas = V(meas) - V(vss)" in instruction
        assert "norm = vhi * clip01(local_meas / span)" in instruction
        assert "span_min <= span <= span_max" in instruction
        assert "above `span_max`" in instruction

        properties = {
            item["id"]: item["observable_contract"]
            for item in _public_contract(task_name)["properties"]
        }
        assert "local_meas / span" in properties[
            "P_NORMALIZE_MEAS_RELATIVE_TO_THE_LOCAL"
        ]
        assert "does not by itself clear clipped norm" in properties[
            "P_CLEAR_NORM_AND_VALID_WHILE_DISABLED"
        ]


def test_affine_calibration_exposes_sampled_update_and_exact_formula() -> None:
    task_names = (
        "284-calibration-affine-transform",
        "784-calibration-affine-transform-testbench",
        "1284-calibration-affine-transform-bugfix",
    )
    for task_name in task_names:
        task = _task(task_name)
        instruction = (task / "public" / "instruction.md").read_text()
        assert "only on" in instruction
        assert "gain_base + gain_span * clip01(V(gain_ctrl) / vhi)" in instruction
        assert "center + gain * (V(raw) - center) + offset" in instruction
        assert "abs(transformed - V(raw)) / resid_fullscale" in instruction

        properties = {
            item["id"]: item["observable_contract"]
            for item in _public_contract(task_name)["properties"]
        }
        assert "only on each rising clk crossing" in properties[
            "P_ON_EACH_RISING_CLOCK_CROSSING_COMPUTE"
        ]
        assert "clip01(abs(transformed - V(raw))" in properties[
            "P_EXPOSE_A_BOUNDED_RESIDUAL_METRIC_FOR"
        ]


def test_reacquire_lock_exposes_count_and_metric_encoding() -> None:
    task_names = (
        "291-event-reacquire-lock-detector",
        "791-event-reacquire-lock-detector-testbench",
        "1291-event-reacquire-lock-detector-bugfix",
    )
    for task_name in task_names:
        task = _task(task_name)
        instruction = (task / "public" / "instruction.md").read_text()
        assert "phase_error" in instruction
        assert "metric_fullscale" in instruction
        assert "phase_error / metric_fullscale" in instruction
        assert "good_count / lock_count" in instruction

        properties = {
            item["id"]: item["observable_contract"]
            for item in _public_contract(task_name)["properties"]
        }
        assert "phase_error <= lock_window" in properties[
            "P_REQUIRE_CONSECUTIVE_IN_WINDOW_FEEDBACK_EDGE"
        ]
        assert "good_count / lock_count" in properties[
            "P_EXPOSE_PHASE_METRIC_AND_STATE_MON"
        ]


def test_generated_monitor_families_replace_task_specific_placeholders() -> None:
    expected = {
        "285-configurable-startup-policy": "abs(x0 - 0.48) / 0.48",
        "286-explicit-replicated-stage-chain": "0.36*x0 + 0.28*x1",
        "287-edge-delay-qualified-driver": "x0 > x1",
    }
    for family, formula in expected.items():
        family_id, slug = family.split("-", 1)
        for task_name in (
            family,
            f"{int(family_id) + 500}-{slug}-testbench",
            f"{int(family_id) + 1000}-{slug}-bugfix",
        ):
            task = _task(task_name)
            instruction = (task / "public" / "instruction.md").read_text()
            contracts = " ".join(
                item["observable_contract"]
                for item in _public_contract(task_name)["properties"]
            )
            assert "task-specific" not in instruction
            assert "task-specific" not in contracts
            assert formula.replace(" ", "") in instruction.replace(" ", "")


def test_sampled_error_monitor_exposes_update_equations() -> None:
    for task_name in (
        "270-sampled-error-update-monitor",
        "770-sampled-error-update-monitor-testbench",
        "1270-sampled-error-update-monitor-bugfix",
    ):
        task = _task(task_name)
        instruction = (task / "public" / "instruction.md").read_text()
        compact = instruction.replace(" ", "")
        assert "V(target)-V(sample)" in compact
        assert "V(sample)+coeff*error" in compact
        assert "abs(error)/err_fullscale" in compact
        assert "stable_count/ready_count" in compact
        assert "enabled rising clock edge" not in instruction


def test_tia_and_track_hold_expose_numeric_metric_contracts() -> None:
    for task_name in (
        "304-common-gate-tia-front-end",
        "804-common-gate-tia-front-end-testbench",
        "1304-common-gate-tia-front-end-bugfix",
    ):
        compact = (_task(task_name) / "public" / "instruction.md").read_text().replace(
            " ", ""
        )
        assert "(V(bias)-bias_min)/(vcm-bias_min)" in compact
        assert "vdd*effective_gain/rz_gain" in compact
        assert "raw_target" in compact

    for task_name in (
        "311-muxed-track-hold-array-readout",
        "811-muxed-track-hold-array-readout-testbench",
        "1311-muxed-track-hold-array-readout-bugfix",
    ):
        compact = (_task(task_name) / "public" / "instruction.md").read_text().replace(
            " ", ""
        )
        assert "vcm+0.15*code" in compact
        assert "held-valid" in compact
        assert "vout" in compact and "vcm" in compact


def test_long_running_families_expose_exact_numeric_contracts() -> None:
    expected = {
        "305": ("1.0+gain_step*code", "donotapplyanadditionalslewstep"),
        "313": ("0.30/(1.0+overdrive/0.030)", "abs(v(vinp)-v(vinn))"),
        "317": ("code*corr_lsb", "cal_0+2*cal_1+4*cal_2+8*cal_3"),
        "323": ("code*200ps", "code*unit_delay_metric"),
        "326": ("(code+1)*200ps", "(vdd-vss)*code/15"),
    }
    for family_id, snippets in expected.items():
        task_root = RELEASE / "tasks"
        for task_dir in sorted(task_root.glob(f"{family_id}-*")) + sorted(
            task_root.glob(f"{int(family_id) + 500}-*")
        ) + sorted(task_root.glob(f"{int(family_id) + 1000}-*")):
            compact = (
                (task_dir / "public" / "instruction.md")
                .read_text()
                .lower()
                .replace(" ", "")
            )
            for snippet in snippets:
                assert snippet in compact


def test_repaired_testbench_bindings_match_reference_trace_names() -> None:
    expected = {
        "517-strongarm-style-latch-comparator-testbench": {
            "DCMPN": "out_n",
            "DCMPP": "out_p",
        },
        "524-clocked-sample-and-hold-testbench": {
            "IN": "in",
            "OUT": "out",
        },
        "527-dwa-dem-encoder-testbench": {
            "clk": "clk_i",
            "vin": "vin_node",
            "code_msb_i[3]": "code_3",
            "code_msb_i[0]": "code_0",
            "cell_en_o[15]": "cell_en_15",
            "cell_en_o[0]": "cell_en_0",
            "ptr_o[15]": "ptr_15",
            "ptr_o[0]": "ptr_0",
        },
        "539-propagation-delay-comparator-testbench": {
            "CLK": "clk",
            "VINN": "vinn",
            "VINP": "vinp",
            "DCMPN": "out_n",
            "DCMPP": "out_p",
            "LP": "lp_int",
            "LM": "lm_int",
            "VSS": "gnd",
            "VDD": "vdd",
            "CLK_1": "clk",
            "CLK_2": "out_p",
        },
        "602-clocked-sine-source-testbench": {
            "VOUT_P": "vinp",
            "VOUT_N": "vinn",
        },
    }

    for task_name, expected_nets in expected.items():
        actual = _binding_nets(task_name)
        for port_ref, net in expected_nets.items():
            assert actual[port_ref] == net
