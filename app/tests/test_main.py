from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_read_usd_variation():
    response = client.get("/v1/usd/2023")
    data = response.json()["data"]
    assert response.status_code == 200
    assert len(data) > 0
    assert data[0]["date"]
    assert data[0]["variation"]
    assert float(data[0]["variation"])


def test_read_usd_variation_wrong_year():
    response = client.get("/v1/usd/49099")
    assert response.status_code == 404
    assert response.json().get("detail") == "Invalid date"


def test_read_usd_variation_year_with_no_data():
    response = client.get("/v1/usd/2030")
    assert response.status_code == 404
    assert response.json().get("detail") == "No data was found"


def test_read_usd_variation_file():
    response = client.get("/v1/usd/2005?filetype=csv")
    assert response.headers.get("content-type") == "text/csv; charset=utf-8"
    assert response.status_code == 200


def test_read_usd_variation_invalid_file():
    response = client.get("/v1/usd/2005?filetype=json")
    assert response.status_code == 404
    assert response.json().get("detail") == "Invalid filetype"
