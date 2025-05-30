from fastapi import FastAPI

from .tasks import router as tasks_router

app = FastAPI()

app.include_router(tasks_router)

@app.get('/healthz')
async def healthz():
    return {'status': 'ok'}
