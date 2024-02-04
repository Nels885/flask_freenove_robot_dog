from flask import url_for


def test_now_ajax(client):
    for url in ["/now/ajax/", url_for("main.now_ajax")]:
        response = client.get(url)
        assert response.status_code == 200


def test_index(client):
    response = client.get("/")
    assert b"- Home</title>" in response.data
    assert response.status_code == 200


def test_status(client):
    for url in ["/status/", url_for("main.status")]:
        response = client.get(url)
        assert b"- Operating state</title>" in response.data
        assert response.status_code == 200


def test_status_ajax(client):
    for url in ["/status/ajax/", url_for("main.status_ajax")]:
        response = client.get(url)
        assert response.status_code == 200


def test_system(client):
    for url in ["/system/", url_for("main.system")]:
        response = client.get(url)
        assert b"- System</title>" in response.data
        assert response.status_code == 200
