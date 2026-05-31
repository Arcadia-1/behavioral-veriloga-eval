from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "runners"))

from run_vabench_release_minimax_baseline import (  # noqa: E402
    anthropic_messages_endpoint,
    auth_header_lines,
    request_payload,
    resolved_api_metadata,
    resolved_auth_header,
    resolved_token_param,
)


def test_mimo_endpoint_uses_max_completion_tokens_by_default() -> None:
    assert (
        resolved_token_param("https://api.mimo-v2.com/v1", "mimo-v2.5-pro", "auto")
        == "max_completion_tokens"
    )


def test_minimax_endpoint_keeps_max_tokens_by_default() -> None:
    assert resolved_token_param("https://api.minimaxi.com/v1", "MiniMax-M2.7", "auto") == "max_tokens"


def test_mimo_endpoint_uses_api_key_header_by_default() -> None:
    assert resolved_auth_header("https://api.mimo-v2.com/v1", "mimo-v2.5-pro", "auto") == "api-key"


def test_minimax_endpoint_keeps_authorization_header_by_default() -> None:
    assert resolved_auth_header("https://api.minimaxi.com/v1", "MiniMax-M2.7", "auto") == "authorization"


def test_auth_header_lines_can_emit_both_headers() -> None:
    assert auth_header_lines("secret", "both") == [
        "Authorization: Bearer secret",
        "api-key: secret",
    ]


def test_payload_uses_selected_token_field_only() -> None:
    payload = request_payload(
        model="mimo-v2.5-pro",
        system_prompt="system",
        prompt="prompt",
        max_tokens=2048,
        temperature=0.0,
        token_param="max_completion_tokens",
    )

    assert payload["max_completion_tokens"] == 2048
    assert "max_tokens" not in payload


def test_anthropic_endpoint_appends_v1_messages() -> None:
    assert (
        anthropic_messages_endpoint("https://token-plan-cn.xiaomimimo.com/anthropic")
        == "https://token-plan-cn.xiaomimimo.com/anthropic/v1/messages"
    )
    assert (
        anthropic_messages_endpoint("https://token-plan-cn.xiaomimimo.com/anthropic/v1")
        == "https://token-plan-cn.xiaomimimo.com/anthropic/v1/messages"
    )


def test_anthropic_metadata_records_messages_api_contract() -> None:
    assert resolved_api_metadata(
        api_format="anthropic",
        base_url="https://token-plan-cn.xiaomimimo.com/anthropic",
        model="mimo-v2.5-pro",
        token_param="auto",
        auth_header="auto",
    ) == ("max_tokens", "x-api-key")
