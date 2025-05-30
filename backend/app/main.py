from fastapi import FastAPI
from pydantic import BaseModel

from .storage import push_tokens

app = FastAPI()

@app.get('/healthz')
async def healthz():
    return {'status': 'ok'}


class PushTokenIn(BaseModel):
    user_id: str
    token: str


@app.post('/users/push-token')
async def save_push_token(data: PushTokenIn):
    push_tokens[data.user_id] = data.token
    return {'status': 'saved'}
