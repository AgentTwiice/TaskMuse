import base64
import hashlib
import hmac
import json
import time
from typing import Any, Dict, Optional

from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# Allow requests from the mobile app during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:19006", "http://localhost:8081"],
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api/v1")

USERS: Dict[str, Dict[str, Any]] = {}
CALENDARS: Dict[str, Dict[str, Any]] = {}

auth_router = APIRouter(prefix="/auth")

SECRET_KEY = "secret"
ACCESS_TOKEN_EXPIRE_SECONDS = 3600
REFRESH_TOKEN_EXPIRE_SECONDS = 86400 * 7


class UserSchema(BaseModel):
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class OAuthCodeSchema(BaseModel):
    code: str


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed


def _jwt_encode(payload: Dict[str, Any]) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    h_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    p_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    msg = f"{h_b64}.{p_b64}".encode()
    sig = base64.urlsafe_b64encode(hmac.new(SECRET_KEY.encode(), msg, hashlib.sha256).digest()).decode().rstrip("=")
    return f"{h_b64}.{p_b64}.{sig}"


def create_access_token(data: Dict[str, Any], expires_seconds: int) -> str:
    payload = data.copy()
    payload["exp"] = int(time.time()) + expires_seconds
    return _jwt_encode(payload)


def decode_token(token: str) -> Dict[str, Any]:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("invalid token")
    h_b64, p_b64, sig = parts
    msg = f"{h_b64}.{p_b64}".encode()
    expected = base64.urlsafe_b64encode(hmac.new(SECRET_KEY.encode(), msg, hashlib.sha256).digest()).decode().rstrip("=")
    if not hmac.compare_digest(expected, sig):
        raise ValueError("invalid signature")
    payload_json = base64.urlsafe_b64decode(p_b64 + "=" * (-len(p_b64) % 4))
    payload = json.loads(payload_json)
    if payload.get("exp", 0) < int(time.time()):
        raise ValueError("expired")
    return payload

@api_router.get('/healthz')
async def healthz():
    return {'status': 'ok'}


@app.middleware('http')
async def inject_user(request: Request, call_next):
    request.state.user = None
    auth = request.headers.get('Authorization')
    if auth and auth.startswith('Bearer '):
        token = auth.split(' ')[1]
        try:
            payload = decode_token(token)
            request.state.user = USERS.get(payload.get('sub'))
        except Exception:
            request.state.user = None
    response = await call_next(request)
    return response


@auth_router.post('/register')
async def register(user: UserSchema):
    if user.email in USERS:
        raise HTTPException(status_code=400, detail='User already exists')
    USERS[user.email] = {
        'id': len(USERS) + 1,
        'email': user.email,
        'password': hash_password(user.password),
    }
    return {'email': user.email}


@auth_router.post('/login', response_model=TokenSchema)
async def login(user: UserSchema):
    stored = USERS.get(user.email)
    if not stored or not verify_password(user.password, stored['password']):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    access = create_access_token({'sub': user.email}, ACCESS_TOKEN_EXPIRE_SECONDS)
    refresh = create_access_token({'sub': user.email, 'refresh': True}, REFRESH_TOKEN_EXPIRE_SECONDS)
    return {'access_token': access, 'refresh_token': refresh, 'token_type': 'bearer'}


@auth_router.post('/google/callback')
async def google_callback(data: OAuthCodeSchema, request: Request):
    user = request.state.user
    if not user:
        raise HTTPException(status_code=401, detail='Not authenticated')
    CALENDARS[user['email']] = {'token': data.code}
    return {'status': 'stored'}


api_router.include_router(auth_router)
app.include_router(api_router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": str(exc)})
