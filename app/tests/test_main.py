from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_read_dolar_data():
    response = client.get("/v1/dollar/2023")
    data = response.json()["data"]
    assert response.status_code == 200
    assert len(data) > 0
    assert data[0]["fecha"]
    assert data[0]["valor"]
