from fastapi.testclient import TestClient
from app.main import app
from app import storage

client = TestClient(app)


def test_save_push_token():
    response = client.post('/users/push-token', json={'user_id': '1', 'token': 'ExpoPushToken[test]'} )
    assert response.status_code == 200
    assert storage.push_tokens['1'] == 'ExpoPushToken[test]'
