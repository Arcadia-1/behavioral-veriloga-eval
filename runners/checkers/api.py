"""Shared checker type contract."""
from __future__ import annotations

from collections.abc import Callable

Checker = Callable[[list[dict[str, float]]], tuple[bool, str]]
