from dataclasses import dataclass
from datetime import datetime, timedelta, time
from typing import List
import pytz


@dataclass
class Task:
    """Simple representation of a task."""

    due: datetime
    duration_minutes: int


@dataclass
class Slot:
    """Represents a calendar slot with start and end times."""

    start: datetime
    end: datetime


def suggest_slots(
    task: Task,
    calendar_events: List[Slot],
    *,
    timezone: str = "UTC",
    work_start: time = time(9, 0),
    work_end: time = time(17, 0),
) -> List[Slot]:
    """Return available time slots for the given task.

    Algorithm steps:
    1. Convert the current time and task due date to the user's timezone using
       ``pytz``.
    2. Iterate over each day between ``now`` and the task's due date.
    3. For every working day, build an initial free block between ``work_start``
       and ``work_end``.
    4. Subtract existing ``calendar_events`` that overlap with the block to
       derive free segments.
    5. Within those segments, collect contiguous blocks that can fit the task's
       ``duration_minutes``. Stop once the due date is reached.
    """

    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    due = task.due.astimezone(tz)
    events = sorted(calendar_events, key=lambda e: e.start)

    result: List[Slot] = []
    day = now.date()
    duration = timedelta(minutes=task.duration_minutes)

    while tz.localize(datetime.combine(day, work_start)) <= due:
        start_of_day = tz.localize(datetime.combine(day, work_start))
        end_of_day = tz.localize(datetime.combine(day, work_end))

        # Skip past days completely in the past
        if end_of_day <= now:
            day += timedelta(days=1)
            continue

        free_blocks = [(max(start_of_day, now), min(end_of_day, due))]

        for event in events:
            # Only consider events happening on this day
            if event.end <= free_blocks[0][0] or event.start >= free_blocks[-1][1]:
                continue
            new_blocks = []
            for block_start, block_end in free_blocks:
                if event.end <= block_start or event.start >= block_end:
                    new_blocks.append((block_start, block_end))
                    continue
                if block_start < event.start:
                    new_blocks.append((block_start, event.start))
                if event.end < block_end:
                    new_blocks.append((event.end, block_end))
            free_blocks = new_blocks

        for block_start, block_end in free_blocks:
            candidate_start = block_start
            while candidate_start + duration <= block_end:
                result.append(Slot(start=candidate_start, end=candidate_start + duration))
                candidate_start += duration

        day += timedelta(days=1)
    return result
