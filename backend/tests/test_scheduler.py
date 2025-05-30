from datetime import datetime, timedelta

import pytz

from services.scheduler import Task, Slot, suggest_slots


def test_suggest_slots_simple():
    tz = pytz.timezone("UTC")
    now = tz.localize(datetime(2024, 1, 1, 9, 0))
    task = Task(due=tz.localize(datetime(2024, 1, 2, 17, 0)), duration_minutes=60)
    events = [
        Slot(
            start=tz.localize(datetime(2024, 1, 1, 9, 0)),
            end=tz.localize(datetime(2024, 1, 1, 10, 0)),
        ),
        Slot(
            start=tz.localize(datetime(2024, 1, 1, 12, 0)),
            end=tz.localize(datetime(2024, 1, 1, 13, 0)),
        ),
    ]
    slots = suggest_slots(task, events, timezone="UTC", work_start=now.time())
    # Expect slots excluding 9-10 and 12-13 on Jan 1
    assert any(
        s.start == tz.localize(datetime(2024, 1, 1, 10, 0)) and
        s.end == tz.localize(datetime(2024, 1, 1, 11, 0))
        for s in slots
    )
    assert all(s.end - s.start == timedelta(minutes=60) for s in slots)
