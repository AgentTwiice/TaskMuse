from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Header, status
from pydantic import BaseModel

router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_datetime: datetime

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_datetime: Optional[datetime] = None

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    due_datetime: datetime
    completed: bool = False
    owner: str

# In-memory storage for tasks
tasks_db: List[Task] = []
next_id = 1


def get_current_user(x_user: Optional[str] = Header(None)) -> str:
    if not x_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return x_user


@router.get('/tasks', response_model=List[Task])
def list_tasks(limit: int = 100, offset: int = 0, user: str = Depends(get_current_user)):
    user_tasks = [t for t in tasks_db if t.owner == user]
    return user_tasks[offset:offset + limit]


@router.post('/tasks', response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, user: str = Depends(get_current_user)):
    if task.due_datetime <= datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='due_datetime must be in the future')
    global next_id
    new_task = Task(id=next_id, owner=user, completed=False, **task.dict())
    next_id += 1
    tasks_db.append(new_task)
    return new_task


@router.put('/tasks/{task_id}', response_model=Task)
def update_task(task_id: int, update: TaskUpdate, user: str = Depends(get_current_user)):
    for t in tasks_db:
        if t.id == task_id and t.owner == user:
            data = update.dict(exclude_unset=True)
            for key, value in data.items():
                setattr(t, key, value)
            return t
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')


@router.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, user: str = Depends(get_current_user)):
    for idx, t in enumerate(tasks_db):
        if t.id == task_id and t.owner == user:
            del tasks_db[idx]
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')


@router.post('/tasks/{task_id}/complete', response_model=Task)
def mark_complete(task_id: int, user: str = Depends(get_current_user)):
    for t in tasks_db:
        if t.id == task_id and t.owner == user:
            t.completed = True
            return t
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found')
