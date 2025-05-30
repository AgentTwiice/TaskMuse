from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_and_login():
    resp = client.post('/api/v1/auth/register', json={'email': 'user@example.com', 'password': 'secret'})
    assert resp.status_code == 200
    resp = client.post('/api/v1/auth/login', json={'email': 'user@example.com', 'password': 'secret'})
    assert resp.status_code == 200
    data = resp.json()
    assert 'access_token' in data and 'refresh_token' in data
    auth = {'Authorization': f"Bearer {data['access_token']}"}
    resp = client.post('/api/v1/auth/google/callback', json={'code': 'abc'}, headers=auth)
    assert resp.status_code == 200
