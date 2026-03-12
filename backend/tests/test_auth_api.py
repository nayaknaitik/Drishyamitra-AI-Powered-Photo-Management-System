from __future__ import annotations


def test_register_and_login(client):
    r = client.post("/auth/register", json={"email": "a@example.com", "password": "pass1234"})
    assert r.status_code == 200
    data = r.get_json()
    assert "access_token" in data

    r2 = client.post("/auth/login", json={"email": "a@example.com", "password": "pass1234"})
    assert r2.status_code == 200
    data2 = r2.get_json()
    assert "access_token" in data2

