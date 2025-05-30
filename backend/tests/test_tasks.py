from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from app.main import app
from app import tasks

client = TestClient(app)


def setup_function(_):
    tasks.tasks_db.clear()
    tasks.next_id = 1


def auth_headers(user: str = "1"):
    return {"X-User": user}


def test_auth_required():
    response = client.get("/tasks")
    assert response.status_code == 401


def test_due_datetime_future_validation():
    past = datetime.utcnow() - timedelta(days=1)
    response = client.post(
        "/tasks",
        json={"title": "t1", "due_datetime": past.isoformat()},
        headers=auth_headers(),
    )
    assert response.status_code == 400


def test_task_crud_flow():
    future = datetime.utcnow() + timedelta(hours=1)
    # create
    response = client.post(
        "/tasks",
        json={"title": "t1", "due_datetime": future.isoformat()},
        headers=auth_headers(),
    )
    assert response.status_code == 201
    task = response.json()
    task_id = task["id"]

    # list
    response = client.get("/tasks", headers=auth_headers())
    assert response.status_code == 200
    assert len(response.json()) == 1

    # update
    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "t1-updated"},
        headers=auth_headers(),
    )
    assert response.status_code == 200
    assert response.json()["title"] == "t1-updated"

    # complete
    response = client.post(f"/tasks/{task_id}/complete", headers=auth_headers())
    assert response.status_code == 200
    assert response.json()["completed"] is True

    # delete
    response = client.delete(f"/tasks/{task_id}", headers=auth_headers())
    assert response.status_code == 204
    response = client.get("/tasks", headers=auth_headers())
    assert response.json() == []


def test_pagination():
    future = datetime.utcnow() + timedelta(hours=1)
    for i in range(5):
        client.post(
            "/tasks",
            json={"title": f"t{i}", "due_datetime": future.isoformat()},
            headers=auth_headers(),
        )
    response = client.get("/tasks?limit=2&offset=1", headers=auth_headers())
    assert response.status_code == 200
    tasks_list = response.json()
    assert len(tasks_list) == 2
    assert tasks_list[0]["title"] == "t1"
