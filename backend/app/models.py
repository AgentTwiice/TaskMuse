from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

import sqlalchemy as sa
from sqlmodel import SQLModel, Field


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(nullable=False, index=True, sa_column_kwargs={"unique": True})
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Calendar(SQLModel, table=True):
    __tablename__ = "calendars"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False)
    provider: str
    access_token: str
    refresh_token: Optional[str] = None
    last_synced: Optional[datetime] = None


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False)
    title: str
    description: Optional[str] = None
    due_datetime: Optional[datetime] = None
    priority: TaskPriority = Field(
        default=TaskPriority.medium,
        sa_column=sa.Column(sa.Enum(TaskPriority, name="taskpriority")),
    )
    calendar_event_id: Optional[str] = None
    status: TaskStatus = Field(
        default=TaskStatus.pending,
        sa_column=sa.Column(sa.Enum(TaskStatus, name="taskstatus")),
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
