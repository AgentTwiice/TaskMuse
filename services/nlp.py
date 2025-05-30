from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import openai


@dataclass
class TaskDraft:
    title: str
    date_iso: str
    time_iso: str
    priority: str


def _call_openai(text: str, timeout: float) -> dict[str, Any]:
    """Internal helper to call OpenAI ChatCompletion."""
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an assistant that extracts task title, date, time, and priority from user input."},
            {"role": "user", "content": text},
        ],
        timeout=timeout,
    )
    return response


def parse_task(text: str, *, retries: int = 3, timeout: float = 10.0) -> TaskDraft:
    """Convert free-form text to a TaskDraft using OpenAI."""
    last_err: Exception | None = None
    for _ in range(retries):
        try:
            resp = _call_openai(text, timeout)
            content = resp["choices"][0]["message"]["content"]
            data = json.loads(content)
            return TaskDraft(
                title=data.get("title", ""),
                date_iso=data.get("date_iso", ""),
                time_iso=data.get("time_iso", ""),
                priority=data.get("priority", ""),
            )
        except Exception as err:  # noqa: BLE001
            last_err = err
    raise last_err if last_err else RuntimeError("Unable to parse task")
