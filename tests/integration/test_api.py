import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def make_user():
    return {
        "firstName": "Alpha",
        "lastName": "Beta",
        "birthYear": 2000,
        "group": "premium",
    }


def test_endpoints(client):
    rv = client.get("/users")
    assert rv.status_code == 200
    assert rv.get_json() == []

    rv = client.post("/users", json=make_user())
    assert rv.status_code == 201
    user = rv.get_json()
    assert user["id"] == 1

    rv = client.get(f"/users/{user['id']}")
    assert rv.status_code == 200

    rv = client.patch(f"/users/{user['id']}", json={"firstName": "Gamma"})
    assert rv.status_code == 200
    assert rv.get_json()["firstName"] == "Gamma"

    rv = client.patch(f"/users/{user['id']}", json={"birthYear": "x"})
    assert rv.status_code == 400

    rv = client.delete(f"/users/{user['id']}")
    assert rv.status_code == 204

    rv = client.get(f"/users/{user['id']}")
    assert rv.status_code == 404

    rv = client.delete("/users/999")
    assert rv.status_code == 404

    rv = client.get("/users/-1")
    assert rv.status_code == 404
    rv = client.delete("/users/0")
    assert rv.status_code == 404

