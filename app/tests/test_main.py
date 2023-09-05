from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_read_dolar_data():
    response = client.get("/dollar")
    data = response.json()["data"]
    assert response.status_code == 200
    assert len(data) > 0
    assert data[0]["date"]
    assert data[0]["value"]
