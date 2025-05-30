from fastapi import APIRouter

router = APIRouter()

@router.get('/tasks')
async def list_tasks():
    return []
